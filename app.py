from flask import Flask, render_template, request, jsonify, send_from_directory
import yt_dlp
import os
import subprocess
import time

app = Flask(__name__)



@app.route("/outro_template")
def outro_template():
    return render_template("outro_template.html")


@app.route("/", methods=["GET", "POST"])
def index():
    # Caminho para a pasta 'static'
    video_folder = os.path.join(app.root_path, 'static')
    
    # Lista os arquivos de vídeo dentro da pasta 'static'
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4') or f.endswith('.webm')]

    if request.method == "POST":
        url = request.form["url"]
        try:
            ydl_opts = {
                'format': 'best',  # Baixa o melhor vídeo até 480p e o melhor áudio
                'outtmpl': 'static/%(id)s.%(ext)s',  # Define o nome do arquivo com base no ID do vídeo
                'noplaylist': True,  # Impede o download de playlists
                'cookiefile': 'cookies.txt',  # Caminho para o arquivo de cookies exportado
            }

            # Baixando o vídeo
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)  # Realiza o download

            # Define o caminho para o arquivo baixado
            video_filename = f"{info_dict['id']}.{info_dict['ext']}"
            video_path = os.path.join('static', video_filename)

            if os.path.exists(video_path):
                return render_template("index.html", videos=video_files, video_url=url, download_success=True, video_path=video_filename)
            else:
                return render_template("index.html", video_url=url, error="Erro ao baixar o vídeo.")

        except Exception as e:
            return render_template("index.html", video_url=url, error=f"Erro: {str(e)}")
    
    return render_template("index.html", videos=video_files)




@app.route("/outro_template", methods=["GET", "POST"])
def index2():
    # Caminho para a pasta 'static'
    video_folder = os.path.join(app.root_path, 'static')
    
    # Lista os arquivos de vídeo dentro da pasta 'static'
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4') or f.endswith('.webm')]

    if request.method == "POST":
        url = request.form["url"]
        try:
            ydl_opts = {
               'format': 'bestvideo[height<=480]+bestaudio/best',  # Baixa o melhor vídeo até 480p e o melhor áudio
                'outtmpl': 'static/%(id)s.%(ext)s',  # Define o nome do arquivo com base no ID do vídeo
                'noplaylist': True,  # Impede o download de playlists
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)  # Realiza o download

            # Define o caminho para o arquivo baixado
            video_filename = f"{info_dict['id']}.{info_dict['ext']}"
            video_path = os.path.join('static', video_filename)

            if os.path.exists(video_path):
                return render_template("outro_template.html", videos=video_files, video_url=url, download_success=True, video_path=video_filename)
            else:
                return render_template("outro_template.html", video_url=url, error="Erro ao baixar o vídeo.")

        except Exception as e:
            return render_template("outro_template.html", video_url=url, error=f"Erro: {str(e)}")
    
    return render_template("outro_template.html", videos=video_files)



@app.route("/remover_videos", methods=["GET"])
def remover_videos():
    try:
        video_folder = os.path.join(app.root_path, 'static')
        # Lista todos os arquivos de vídeo (.mp4, .webm) na pasta 'static'
        video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.webm'))]

        # Remove cada arquivo de vídeo encontrado
        for video in video_files:
            video_path = os.path.join(video_folder, video)
            os.remove(video_path)
            os.remove(video_path+".mp4")
        
        return jsonify({"success": True, "message": "Vídeos removidos com sucesso!"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Erro ao remover vídeos: {str(e)}"}), 500




@app.route("/delete_video/<filename>", methods=["POST"])
def delete_video(filename):
    video_path = os.path.join(app.root_path, 'static', filename)
    if os.path.exists(video_path):
        os.remove(video_path)
        os.remove(video_path+".mp4")
        return jsonify({"success": True, "message": "Vídeo apagado com sucesso!"}), 200
    return jsonify({"success": False, "message": "Arquivo não encontrado!"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Pega a porta do ambiente, ou usa 5000 como padrão
    app.run(host='0.0.0.0', port=port)
