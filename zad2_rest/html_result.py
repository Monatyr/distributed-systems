

def create_html(data):
    file_path = f"templates/{data['data'][0]['artist'].lower().replace(' ', '_')}_{data['type']}.html"
    file = open(file_path, 'w')
    file.write('<!DOCTYPE html>\n<html>\n<head>\n')
    #head
    file.write('\t<meta charset="UTF-8">\n\t<title>Search result</title>')
    #/head
    file.write('</head>\n')

    file.write('<style>\ntable, th, td {\n border:1px solid black;\n}\n</style>\n')

    file.write('<body>\n')
    #body
    if data['type'] == 'albums':
        file.write('<table style="width:100%">\n')
        file.write('<tr>\n<th>Album</th>\n<th>Number of tracks</th>\n<th>Release date</th>\n<th>Cover</th>\n</tr>')
        for album in data['data']:
            file.write(f'<tr>\n<td>{album["name"]}</td>\n<td>{album["tracks"]}</td>\n<td>{album["release_date"]}</td>\n<td><img src={album["image"]} width=100></td>\n</tr>\n')
    elif data['type'] == 'artist_songs':
        file.write('<table style="width:100%">\n')
        file.write('<tr>\n<th>Song</th>\n<th>Album</th>\n<th>Length</th>\n<th>Cover</th>\n</tr>')
        for song in data['data']:
            file.write(f'<tr>\n<td>{song["name"]}</td>\n<td>{song["album"]}</td>\n<td>{song["time_length"]}</td>\n<td><img src={song["image"]} width=100></td>\n</tr>\n')
    file.write('</body>\n')
    file.write('</html>')
    file.close()
    print(file_path)
    return file_path