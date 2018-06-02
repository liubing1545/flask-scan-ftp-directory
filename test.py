import os

def delete():
    item ="n-444444-ENG-Word-10705-180331122039488.wav"
    
    array = item.split('-')
    if len(array) != 6:
        abort(500)

    file_path = '%s/%s/%s/%s/%s/%s' % ('/home/ftper/ftp_root/resource', array[2], array[1], array[3], array[4], item)
    if os.path.exists(file_path):
        os.remove(file_path)    
        #return jsonify({'deleted': file_name})



if __name__ == '__main__':
    #db.create_all()
    delete()