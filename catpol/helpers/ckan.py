from ckanapi import RemoteCKAN

from catpol.settings import CKAN_HOST, CKAN_API_TOKEN

# Generic variables
ua = 'ckanapiexample/1.0 (+http://example.com/my/website)'


def connect_to_remote(host=CKAN_HOST, api_key=CKAN_API_TOKEN):
    """Return a valid connect to the CKAN."""
    try:
        conn = RemoteCKAN(host, apikey=api_key, user_agent=ua)
    except Exception as ex:
        print 'Unable to connect to %s due to %s' % (host, ex)
        exit(1)
    else:
        print 'Connected!'

    return conn


def upload_to_remote(conn, file_path, file_name):
    """Upload function for CKAN 2.2+.

    Will use the file_name to label the package_id.
    """
    try:
        conn.action.resource_create(
            package_id=file_name,
            url=file_name,  # ignored but required by CKAN<2.6
            upload=open(file_path, 'rb'))
    except Exception as ex:
        print 'Unable to upload %s due to %s' % (file_name, ex)
    else:
        print 'Uploaded: %s' % file_path


def upload_to_remote_alternative(conn, file_path, file_name):
    """Upload function using call_action."""
    try:
        conn.call_action('resource_create',
            {'package_id': file_name},
            files={'upload': open(file_path, 'rb')})
    except Exception as ex:
        print 'Unable to upload %s due to %s' % (file_name, ex)
    else:
        print 'Uploaded: %s' % file_path


def close_connection(conn):
    """Make sure you close the connection."""
    try:
        conn.close()
    except Exception as ex:
        print 'Unable to close the connection to %s because %s' % (conn, ex)
    else:
        print 'Closed remote connection'
