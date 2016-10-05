package luke.com.fiirapp;

import android.os.Environment;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.net.HttpURLConnection;

import java.net.URL;
import java.util.ArrayList;

/**
 * Created by luke on 10/5/16.
 *
 * Simple wrapper for sending POST requests to fiir API
 */

public class ApiRequest {
    PostRequest post;
    String key;
    String userid;

    public ApiRequest(String url){
        this.post = new PostRequest(url);
    }

    public void setCredentials(String key, String userid){
        this.key = key;
        this.userid = userid;
    }

    public String[] users_create(String phone, String invitedby, String email){
        return post.execute("/users/create", phone, invitedby, email);
    }
    public String[] users_setPromo(String promoCode){
        return post.execute("/users/setPromo", key, userid, promoCode);
    }
    public String[] pics_create(String price, String token){
        return post.execute("/pics/create", key, userid, price, token);
    }
    public String[] pics_created(){
        return post.execute("/pics/created", key, userid);
    }
    public String[] pics_flag(String pictureId){
        return post.execute("pics/flag", key, userid, pictureId);
    }
    public String[] pics_hide(String pictureId){
        return post.execute("pics/hide", key, userid, pictureId);
    }
    public String[] friends_list(){
        return post.execute("friends/list", key, userid);
    }
    public String[] friends_add(String friendId){
        return post.execute("friends/add", key, userid, friendId);
    }
    public String[] friends_remove(String friendId){
        return post.execute("friends/remove", key, userid, friendId);
    }
    public String[] settings_updateEmail(String email){
        return post.execute("settings/update_email", key, userid, email);
    }
    public String[] settings_updatePhone(String phone){
        return post.execute("/settings/update_phone", key, userid, phone);
    }

    private class PostRequest{
        String url;

        public PostRequest(String url){
            this.url = url;
        }

        // TODO add additional post params from varargs and parse response json to String[]
        public String[] execute(String endpoint, String...args){
            HttpURLConnection connection = null;
            DataOutputStream outputStream = null;
            DataInputStream inputStream = null;
            String pathToOurFile = "/data/file_to_send.mp3";
            String urlServer = "http://192.168.1.1/handle_upload.php";
            String lineEnd = "\r\n";
            String twoHyphens = "--";
            String boundary =  "*****";

            int bytesRead, bytesAvailable, bufferSize;
            byte[] buffer;
            int maxBufferSize = 1*1024*1024;

            try{
                FileInputStream fileInputStream = new FileInputStream(new File(pathToOurFile) );

                URL url = new URL(urlServer);
                connection = (HttpURLConnection) url.openConnection();

                // Allow Inputs &amp; Outputs.
                connection.setDoInput(true);
                connection.setDoOutput(true);
                connection.setUseCaches(false);

                // Set HTTP method to POST.
                connection.setRequestMethod("POST");

                connection.setRequestProperty("Connection", "Keep-Alive");
                connection.setRequestProperty("Content-Type", "multipart/form-data;boundary="+boundary);

                outputStream = new DataOutputStream( connection.getOutputStream() );
                outputStream.writeBytes(twoHyphens + boundary + lineEnd);
                outputStream.writeBytes("Content-Disposition: form-data; name=\"uploadedfile\";filename=\"" + pathToOurFile +"\"" + lineEnd);
                outputStream.writeBytes(lineEnd);

                bytesAvailable = fileInputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];

                // Read file
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0)
                {
                    outputStream.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                }

                outputStream.writeBytes(lineEnd);
                outputStream.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);

                // Responses from the server (code and message)
                int serverResponseCode = connection.getResponseCode();
                String serverResponseMessage = connection.getResponseMessage();

                fileInputStream.close();
                outputStream.flush();
                outputStream.close();
            }
            catch (Exception e){
                //Exception handling
            }

            return new String[]{};
        }

    }
}// end class ApiRequest
