from astropy.table import Table
from numpy import array, copy, append, round, reshape


class Bin:
    def __init__(self, objects=None, object_column_names=None, bin_params=None, bin_param_names=None):
        """
        :param objects: The objects contained in the bin.
        :param object_column_names: The column names when the objects are sorted column-wise instead of row-wise.
        :param bin_params: The bin widths.
        """
        if bin_params is None:
            bin_params = []
        if bin_param_names is None:
            bin_param_names = []

        self.objects = objects
        self.object_column_names = object_column_names
        self.bin_params = bin_params
        self.bin_param_names = bin_param_names

    def rebin(self, param_index, low_bounds, bin_width, number_threshold=4):
        """
        Returns a list of Bin objects after re-binning based on a certain value and bin parameters.
        Bins specified by the lower bounds and bin width.
        :param param_index: Which index in the objects contains the desired value.
        :param low_bounds: Lower bounds on the bins.
        :param bin_width: The width of the bins.
        :param number_threshold: The required number of objects a bin needs to have to be saved to the list.
        :return: List of re-binned Bin objects.
        """
        new_bins = []
        top_level_params = self.bin_params
        top_level_param_names = self.bin_param_names

        for low in low_bounds:
            this_bin = []

            for obj in self.objects:
                if low < obj[param_index] < low + bin_width:
                    this_bin.append(obj)
            if len(this_bin) <= number_threshold:
                continue

            new_bin = Bin(objects=this_bin, object_column_names=self.object_column_names,
                          bin_params=append(copy(top_level_params), (round(low, 2), round(low + bin_width, 2))),
                          bin_param_names=append(copy(top_level_param_names), self.key_from_index(param_index)))
            new_bins.append(new_bin)

        return new_bins

    def return_columns(self):
        """
        Returns a dictionary of columns (turns the object list back into a column format)
        """
        keys = copy(self.object_column_names)
        columns = []
        for i in range(0, len(keys)):
            columns.append([])
            for j in range(0, len(self.objects)):
                columns[i].append(self.objects[j][i])

        return list(keys), columns

    def index_from_key(self, key=""):
        """ Return the index of the column name key specified."""
        return self.object_column_names.index(key)

    def key_from_index(self, index=0):
        return self.object_column_names[index]

    def values_in_bin(self, values):
        """
        Returns a boolean whether of not a set of values is within the bin.
        :param values: A list of values.
        :return:
        """
        reshaped_values = reshape(self.bin_params, newshape=(int(len(self.bin_params) / 2), 2))
        good_count = 0
        for i in range(0, len(values)):
            if reshaped_values[i][0] < values[i] < reshaped_values[i][1]:
                good_count += 1

        if good_count == len(values):
            return True
        else:
            return False

    def return_param_dict(self):
        """
        Returns a dict object where the keys are the column names that built the parameter set,
        and the values are the corresponding parameters.
        """
        param_dict = {}
        for i in range(0, len(self.bin_param_names)):
            param_dict[self.bin_param_names[i]] = (self.bin_params[2 * i], self.bin_params[2 * i + 1])
        return param_dict


def select_bin(bin_list, values):
    for b in bin_list:
        if b.values_in_bin(values):
            return b
    return None


def generate_objects(params):
    """
    Reorganizes the table columns into an object-format
    :param params: A list of table columns
    :return:
    """
    objects = []
    for i in range(0, len(params[0])):
        this_obj = []
        for j in range(0, len(params)):
            this_obj.append(params[j][i])
        objects.append(this_obj)
    return objects


def bin_catalog(config_values):
    """
    Bin the inputted catalog.
    :param catalog_filename: Catalog of objects.
    :param config_values: Values from inputted config file or user inputs.
    :return: full_bins - a list of Bin objects for further processing
    """

    # Read HST-ZEST catalog into memory
    catalog = Table.read(config_values["CATALOG"], format="fits")

    mags = array(catalog[config_values["MAG_KEY"]])
    r50s = array(catalog[config_values["R50_KEY"]])
    ns = array(catalog[config_values["N_KEY"]])
    ellips = array(catalog[config_values["ELLIP_KEY"]])
    masses = array(catalog[config_values["MASS_KEY"]])
    sfprobs = array(catalog[config_values["SFPROB_KEY"]])
    redshifts = array(catalog[config_values["Z_KEY"]])

    mass_bins, mass_step = config_values["MASS_BINS"], config_values["MASS_STEP"]
    redshift_bins, redshift_step = config_values["REDSHIFT_BINS"], config_values["REDSHIFT_STEP"]
    sfprob_bins, sfprob_step = config_values["SFPROB_BINS"], config_values["SFPROB_STEP"]

    catalog_objects = generate_objects((mags, r50s, ns, ellips, masses, redshifts, sfprobs))
    column_names = ["MAGS", "R50S", "NS", "ELLIPS", "MASSES", "REDSHIFTS", "SFPROBS"]
    init_bin = Bin(objects=catalog_objects, object_column_names=column_names, bin_params=[])

    mass_bins = init_bin.rebin(4, mass_bins, mass_step)
    mz_bins, full_bins = [], []
    for cat_bin in mass_bins:
        mz_bins.extend(cat_bin.rebin(5, redshift_bins, redshift_step))
    for cat_bin in mz_bins:
        full_bins.extend(cat_bin.rebin(6, sfprob_bins, sfprob_step))

    return full_bins


def bin_mag_catalog(mag_table, b, mag_table_keys=None, bin_keys=None):
    """
    Bin an external catalogue based on a bin's provided parameters.
    :param mag_table The magnitude table to rebin
    :param b The tbridge.Bin object
    :param mag_table_keys The magnitude table keys to use for binning.
    :param bin_keys The associated bin keys (must be the same length AND order as mag_table_keys).
    """
    if bin_keys is None:
        bin_keys = ["MASSES", "REDSHIFTS"]
    if mag_table_keys is None:
        mag_table_keys = ["MASS", "Z"]

    # Gather the necessary information from the provided bin.
    bin_dict = b.return_param_dict()

    # Iterate over all keys and only return the rows that are within the bin limits.
    for i in range(len(bin_keys)):
        low, high = bin_dict[bin_keys[i]]
        mag_table = mag_table[mag_table[mag_table_keys[i]] >= low]
        mag_table = mag_table[mag_table[mag_table_keys[i]] <= high]

    return mag_table