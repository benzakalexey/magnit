from waitress import serve
from magnit.composites import api
serve(api.app, host='0.0.0.0', port=8080)
