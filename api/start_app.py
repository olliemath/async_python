from __future__ import absolute_import
from api.patch import patch_db_conn

patch_db_conn()

from api.app import app  # noqa: E402


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
