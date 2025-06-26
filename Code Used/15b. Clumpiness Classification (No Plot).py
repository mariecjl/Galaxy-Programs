# import utils.plot as pu
# import utils.image as iu
import numpy as np
from scipy import stats
from photutils.aperture import EllipticalAperture, CircularAperture

from photutils.aperture import CircularAperture, EllipticalAperture
from photutils.aperture import aperture_photometry as aperPhot

import matplotlib.pyplot as plt
import matplotlib as mpl


def round_to_base(array, base=10):
    return [base * round(x / base) for x in array]


def mode(array, base):
    rounded = round_to_base(array, base=base)
    return stats.mode(rounded, keepdims=False)[0]


def _ellip_params(centric_dist, centric_ang):
    pa = np.deg2rad(mode(centric_ang, base=20))
    min_ax = mode(centric_dist, base=2)
    maj_ax = max(centric_dist)
    eccentricity = 1 - min_ax / maj_ax
    return maj_ax, min_ax, pa, eccentricity


def _centric_distang(segmap, center):
    gal_mask = segmap.ravel() == 1

    yi, xi = np.indices(segmap.shape)
    lm_yc, lm_xc = center

    centric_dis = np.sqrt((yi - lm_yc) ** 2 + (xi - lm_xc) ** 2)
    centric_dis = centric_dis.ravel()[gal_mask]

    centric_ang = np.rad2deg(np.arctan2((yi - lm_yc), (xi - lm_xc)))
    centric_ang = centric_ang.ravel()[gal_mask]
    centric_ang[centric_ang < 0] += 180
    return centric_dis, centric_ang


def mask_zeros(img, isbool=False):
    mask = img.copy()

    if isbool:
        mask = mask.astype(float)

    mask[mask == 0] = np.nan
    return mask


def _max_dist_cutoff(segmap, center, galparams):
    galmask = mask_zeros(segmap, isbool=True)
    maj_ax, min_ax, pa, eccentricity = galparams

    eccens = np.linspace(0, 0.8, 9)
    apertures = [
        EllipticalAperture(center, min_ax / (1 - e), min_ax, pa) for e in eccens
    ]

    aper_masks = [
        mask_zeros(aperture.to_mask(method="center").to_image(galmask.shape))
        for aperture in apertures
    ]

    pixcount_ratios = [
        np.isfinite(aper_mask * galmask).sum() / np.isfinite(aper_mask).sum()
        for aper_mask in aper_masks
    ]

    try:
        max_e_idx = np.argwhere(np.array(pixcount_ratios) > 0.95).ravel()[-1]
        max_e = eccens[max_e_idx]
        max_dist = min_ax / (1 - max_e)
    except IndexError:
        print("Error calculating max distance cutoff.")
        max_dist = 30

    return max_dist


class Galaxy:
    def __init__(self, galparams: dict, maps: dict):
        self.maps = maps
        self.segmap = maps["segmap"]
        self.galparams = galparams

        self._galparams()
        # print(self.pa, self.maj_ax, self.e)

    def _mass_weighted_center(self):
        mass_map = self.maps["mass"]
        img_size = mass_map.shape[0]

        self.yi, self.xi = np.indices(mass_map.shape)

        center = (img_size / 2, img_size / 2)
        aperture = CircularAperture(
            center, r=(0.5 / 0.04) / 2.0
        )  # aperture of diameter 0.5"
        mask = aperture.to_mask(method="center").to_image(mass_map.shape)
        mask[mask == 0] = np.nan
        masked_mass = mask * mass_map

        #changed added here
        #if np.isnan(masked_mass).all() or (masked_mass == 0).all():
            #return "NaN or zero"
        
        self.lm_xc = np.nansum(self.xi * masked_mass) / np.nansum(masked_mass)
        self.lm_yc = np.nansum(self.yi * masked_mass) / np.nansum(masked_mass)

        return self.xi, self.yi, self.lm_xc, self.lm_yc, img_size

    def _galparams(self):
        xi, yi, lm_xc, lm_yc, img_size = self._mass_weighted_center()

        center = (lm_xc, lm_yc)
        segmap = self.maps["segmap"].copy()

        centric_dis, centric_ang = _centric_distang(segmap, center)
        init_galparams = _ellip_params(centric_dis, centric_ang)

        max_dist = _max_dist_cutoff(segmap, center, init_galparams)
        centric_ang = centric_ang[centric_dis < max_dist]
        centric_dist = centric_dis[centric_dis < max_dist]
        maj_ax, min_ax, pa, eccentricity = _ellip_params(centric_dist, centric_ang)

        self.galparams["xy"] = center
        self.galparams["pa"] = pa
        self.galparams["maj_ax"] = maj_ax
        self.galparams["e"] = eccentricity

        # plt.subplots(1, 3, figsize=(12, 4))
        # aperEllip = EllipticalAperture(center, maj_ax, maj_ax*(1 - eccentricity), pa)
        # plt.subplot(131)
        # plt.imshow(np.log10(self.maps["mass"]), origin="lower")
        # aperEllip.plot(color='red')

        # plt.subplot(132)
        # plt.hist(centric_ang, bins=9, density=True)

        # plt.subplot(133)
        # plt.hist(centric_dist, bins=15, density=True)
        # plt.show()

    def _get_galparams(self):
        return self.galparams


class NormalizedMaps(Galaxy):
    def __init__(self, galparams, maps):
        Galaxy.__init__(self, galparams, maps)

    def _set_mapType(self, mapType):
        self._map = self.maps[mapType]

    def _umv_ravel(self):
        umv = self.maps["UmV"].ravel()
        # nan_mask = ~np.isnan(umv)
        return umv

    def _normalize_values(self):
        self._get_effective_radius()
        xi, yi, lm_xc, lm_yc, img_size = self._mass_weighted_center()
        centric_distances = np.sqrt(
            (self.yi - self.lm_yc) ** 2 + (self.xi - self.lm_xc) ** 2
        )
        centric_distances = centric_distances.ravel()

        self.values = self._map.ravel()
        self.values = np.where(
            self.values > 0, self.values, np.nan
        )  # Replace invalid values with NaN

        self.radii = centric_distances
        self.radii[np.isnan(self.values)] = np.nan

        self.norm_values = np.log10(self.values / self.norm)
        self.norm_radii = np.log10(self.radii / self.reff)

        # print(lm_xc, lm_yc)
        # print(self.norm, np.nanmax(self.values), self.reff)
        # plt.imshow(self.norm_values.reshape((img_size, img_size)), origin="lower")
        # plt.axvline(x=img_size / 2)
        # plt.axhline(y=img_size / 2)
        # plt.scatter([lm_xc], [lm_yc], marker="x", color="tab:red")
        # plt.show()

    def _get_effective_radius(self):
        galparams = self._get_galparams()
        mass_xy = galparams["xy"]
        pa, maj_ax, eccen = galparams["pa"], galparams["maj_ax"], galparams["e"]

        weighted_map = self.maps["weighted_map"]

        radii = np.arange(1.5, maj_ax, 0.5)
        apertures = [
            EllipticalAperture(mass_xy, sma, sma * (1 - eccen), theta=pa)
            for sma in radii
        ]
        phot_table = aperPhot(self._map, apertures, mask=np.isnan(self._map))

        aperNames = phot_table.colnames[3:]
        aperFluxes = [phot_table[name].data[0] for name in aperNames]
        aperAreas = [aperture.area for aperture in apertures]

        weighted_phot_table = aperPhot(
            self._map / weighted_map, apertures, mask=np.isnan(self._map)
        )
        weightedFluxes = [weighted_phot_table[name].data[0] for name in aperNames]

        maxidx = np.argmax(weightedFluxes[:])  # tmpidx
        reff_idx = np.argmin(abs(weightedFluxes - max(weightedFluxes) / 2.0)) + 1
        self.reff = radii[reff_idx]
        self.norm = aperFluxes[reff_idx] / aperAreas[reff_idx]

        # mask = apertures[maxidx].to_mask(method="center")
        # plt.subplots(1, 2, figsize=(8, 4))
        # plt.subplot(121)
        # plt.imshow(mask.multiply(self._map), origin="lower")
        # plt.subplot(122)
        # plt.scatter(radii, weightedFluxes)
        # plt.show()

    def map_clump(self, mapType):
        self._set_mapType(mapType)
        self._normalize_values()
        self.galparams[f"{mapType}_reff"] = self.reff

        self.inner_idx = self.norm_radii <= -0.5
        self.clump_idx = (self.norm_radii > -0.5) & (
            self.norm_values > 0.06 - 1.6 * self.norm_radii - self.norm_radii**2
        )
        self.outer_idx = (self.norm_radii > -0.5) & (
            self.norm_values <= 0.06 - 1.6 * self.norm_radii - self.norm_radii**2
        )

        # TODO: quick fix right now - this is to mask out area
        # greater than 2.5 reff
        ellipAper = EllipticalAperture(
            self.galparams["xy"],
            2.5 * self.reff,
            2.5 * self.reff * (1 - self.galparams["e"]),
            theta=self.galparams["pa"],
        )
        size = int(np.sqrt(len(self.norm_radii)))
        aperMask = ellipAper.to_mask(method="exact").to_image((size, size)).astype(bool)
        aperMask = np.invert(aperMask)
        galMask = self.maps["segmap"]
        mask = np.logical_and(galMask, aperMask)
        cutoff_idx = mask.ravel() == 1

        self.pixel_types = np.zeros(len(self.norm_radii)) * np.nan
        self.pixel_types[self.inner_idx] = 0
        self.pixel_types[self.clump_idx] = 2
        self.pixel_types[self.outer_idx] = 1
        self.pixel_types[cutoff_idx] = 1
        self.pixel_types[np.isnan(self.norm_values)] = np.nan

        # umv = self._umv_ravel()
        # order = np.argsort(umv)[::-1]

        normprofile = {}
        normprofile["norm_radii"] = self.norm_radii  # [order]
        normprofile["norm_values"] = self.norm_values  # [order]
        normprofile["pixel_types"] = self.pixel_types  # [order]
        # normprofile["colors"] = umv  # [order]

        # plotting normalized profile
        profile_x = np.arange(-0.5, 2.0, 0.1)
        profile_y = 0.06 - 1.6 * profile_x - profile_x**2

        # plotting
        #plt.subplots(1, 2, figsize=(10, 4))

        #plt.subplot(121)
        galparams = self._get_galparams()
        maj_axis = 2 * galparams[f"{mapType}_reff"]
        ellipse = EllipticalAperture(
            galparams["xy"],
            maj_axis,
            maj_axis * (1 - galparams["e"]),
            galparams["pa"],
        )
        #plt.imshow(self._map, origin="lower")
        #plt.title(f"{mapType} map")

        ellipse.plot(color="red")

        #plt.subplot(122)
        cmap = mpl.colors.ListedColormap(["red", "darkgrey", "gold"])
        # plt.scatter(
        #     self.norm_radii,
        #     self.norm_values,
        #     c=self.pixel_types,
        #     cmap=cmap,
        #     vmax=2,
        # )

        # plt.axvline(x=-0.5, linestyle=":", color="black")
        # plt.plot(profile_x, profile_y, linestyle=":", color="black")
        # plt.xlim([-2, 1])
        # plt.ylim([-2, 1])
        # plt.ylabel(r"$\log(\Sigma/\Sigma_e)$")
        # plt.xlabel(r"$\log(R/R_e)$")
        # # plt.colorbar()
        # plt.show()

        return normprofile

    def fraction_in_clump(self):
        sum_clump = np.sum(self.values[self.pixel_types == 2])
        sum_total = np.nansum(self.values)
        # print (sum_clump, sum_total)
        return sum_clump / sum_total

    def is_clumpy(self, mapTypes=["mass"], plot_profiles=False):
        self.plot_profiles = plot_profiles

        isclumpy_dict = {}
        normprofiles = {}
        for mapType in mapTypes:
            print(f"Calculating clumpiness for {mapType}")
            normprofiles[mapType] = self.map_clump(mapType)
            isclumpy_dict[f"{mapType}_isclumpy"] = (
                True if self.fraction_in_clump() > 0.05 else False
            )

        # if self.plot_profiles:
        #     pu.plot_resolved_maps(
        #         self.maps,
        #         isclumpy_dict,
        #         normprofiles=normprofiles,
        #         galparams=self._get_galparams(),
        #     )

        return isclumpy_dict

    def get_mass(self):
        mass = self.maps["mass"]

        lm = np.log10(np.nansum(mass))

        return lm
