
def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions
