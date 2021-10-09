from manage import manager
# app = manager.app


if __name__ == '__main__':
    manager.app.run(host="localhost", port=8000,debug=False, use_reloader=False)
