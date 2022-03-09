import TIFFs.parse


# TODO partition tiff by file size
def _partition_tiff_by_size(path, size, result_path):
    """
    partition given tiff by size to new tiffs
    :param path: path of tiff
    :param size: size of partitioned tiffs
    :param result_path: folder path of result
    :return: status code
    """


# TODO partition tiff by geographic bound to file
def _partition_tiff_by_bound_2file(path, scope, result_path):
    """
    partition given tiff by geographic scope to a new tiff
    :param path: path of tiff
    :param scope: geographic scope of partitioned tiff(rectangle)
    :param result_path: file path of result
    :return: status code
    """


# TODO partition tiff by geographic bound to memory
def _partition_tiff_by_bound_2memory(path, scope, result_type):
    """
    partition given tiff by geographic scope to memory
    :param path: path of tiff
    :param scope: geographic scope of partitioned tiff(rectangle)
    :param result_type: result value type
    :return: data
    """


# TODO partition tiff by image range to file
def _partition_tiff_by_range_2file(path, range, result_path):
    """
    partition given tiff by image range to a new tiff
    :param path: path of tiff
    :param range: image range of partitioned tiff(rows and columns)
    :param result_path: file path of result
    :return: status code
    """


# TODO partition tiff by image range to memory
def _partition_tiff_by_range_2memory(path, range, result_type):
    """
    partition given tiff by image range to memory
    :param path: path of tiff
    :param range: image range of partitioned tiff(rows and columns)
    :param result_type: result value type
    :return: data
    """