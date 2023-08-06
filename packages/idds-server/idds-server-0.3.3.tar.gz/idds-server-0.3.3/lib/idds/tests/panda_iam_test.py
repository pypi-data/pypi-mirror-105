
import pandatools.idds_api
import idds.common.utils as idds_utils

c = pandatools.idds_api.get_api(idds_utils.json_dumps, idds_host='https://aipanda160.cern.ch:443/idds', compress=True, manager=True)

# print(dict(c))
idds_request = {'request_id': 27}

ret = c.abort(request_id=27)
print(ret)

# ret = c.resume(request_id=27)
print(ret)

# ret = c.retry(request_id=27)
print(ret)
