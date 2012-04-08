"""

    Download and install binaries.

    Provide file fecth utilities with some user friendly output through logging API.

"""

# Python imports
import os
import tarfile

# Third party
import requests


def download(logger, towhere, url):
    """ Download file to a specific location on the disk.

    :param towhere: Full path to the download location

    :param url: From where to download

    :return: True if file was already downloaded 
    """
    

    if os.path.exists(towhere):
        return False

    response = requests.get(url)

    #if os.path.exists(towhere):
    #   
    #   # Check that if the file already exist and has correct size
    #   size = response.headers.get("content-length", -1)
    #   
    #       if size != -1 and os.path.getsize(towhere) == size:
    #       return True
    
        
    logger.info("Downloading %s", url)
    
    # Download
    f = open(towhere, "wb")

    # http://docs.python-requests.org/en/latest/api/#requests.Response
    for chunk in response.iter_content():
        f.write(chunk)
    
    f.close()

    return False

def download_and_extract_java_dep(logger, towhere, url):
    """
    Download and extract Java dependency.

    If it's gz unzip, otherwise leave as is.
    """
    download(logger, towhere, url)

    # Extract path

    # W:100,10:download_and_extract_gz: Unused variable 'ext'
    # pylint: disable = W0612
    path = os.path.dirname(towhere)
    fname = os.path.basename(towhere)
    base, ext = os.path.splitext(fname)
    folder = os.path.join(path, base) 

    # XXX: Argh do this again with less coffee more sleep
    folder = folder.replace(".tar", "")

    if towhere.endswith(".gz") and not os.path.exists(folder):
        logger.info("Extracting tar archive: %s to %s" % (fname, folder))

        os.makedirs(folder)

        tar = tarfile.open(towhere)
        tar.extractall(path=folder)
        tar.close()

def download_and_extract_gz(logger, towhere, url):
    """
    Download and extract .tar.gz archive.
    Will be extracted to a folder with matching name.

    :param towhere: Path where the downloaded file is stored
    """

    assert towhere.endswith(".tar.gz"), "You must give a local .tar.gz file"

    # Don't redownload files if they happen to exist
    if not os.path.exists(towhere):
        # XXX: this might be a bad idea due to unfinishe downloads
        download(logger, towhere, url)

    # Extract path
    # W:100,10:download_and_extract_gz: Unused variable 'ext'
    # pylint: disable = W0612    
    path = os.path.dirname(towhere)
    fname = os.path.basename(towhere)
    base, ext = os.path.splitext(fname)
    folder = os.path.join(path, base) 

    # XXX: Argh do this again with less coffee more sleep
    folder = folder.replace(".tar", "")

    logger.debug("Extracting tar archive: %s to %s" % (fname, folder))

    os.makedirs(folder)

    tar = tarfile.open(towhere)
    tar.extractall(path=folder)
    tar.close()


