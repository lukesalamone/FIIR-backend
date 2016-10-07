package luke.com.fiirapp;

import android.os.Environment;
import android.util.Log;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;

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
        JSONObject params = new JSONObject();
        try {
            params.put("phone", phone);
            params.put("invitedby", new Integer(invitedby));
            params.put("email", email);
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("/users/create", params);
    }
    public String[] users_setPromo(String promoCode){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("promoCode", promoCode);
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("/users/setPromo", params);
    }
    // TODO
    public String[] pics_create(String filepath, String price, String token){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("file", filepath);
            params.put("price", new Integer(price));
            params.put("token", token);
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("/pics/create", params);
    }
    public String[] pics_created(){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("/pics/created", params);
    }
    public String[] pics_flag(String pictureId){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("pictureId", new Integer(pictureId));
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("pics/flag", params);
    }
    public String[] pics_hide(String pictureId){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("pictureId", new Integer(pictureId));
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("pics/hide", params);
    }
    public String[] friends_list(){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
        } catch (JSONException e){
            e.printStackTrace();
            return new String[]{"JSON exception"};
        }
        return post.execute("friends/list", params);
    }
    /*
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
*/
    private class PostRequest{
        String baseUrl;
        URL url;
        public PostRequest(String baseUrl){
            this.baseUrl = baseUrl;
        }

        public String[] execute(String endpoint, JSONObject params){
            try {
                url = new URL(this.baseUrl + endpoint);
                Log.i("sending to url", url.toString());
            }catch(MalformedURLException e){
                return new String[]{"Malformed url: " + this.baseUrl + endpoint};
            }

            ArrayList<String> response = new ArrayList<>();
            try {
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setReadTimeout(15000);
                conn.setConnectTimeout(15000);
                conn.setRequestMethod("POST");
                conn.setDoInput(true);
                conn.setDoOutput(true);

                OutputStream os;
                try{
                    os = conn.getOutputStream();
                } catch(java.net.ConnectException e){
                    e.printStackTrace();
                    return new String[]{"Error: connection refused"};
                }
                BufferedWriter writer = new BufferedWriter(
                        new OutputStreamWriter(os, "UTF-8"));
                writer.write(params.toString());

                writer.flush();
                writer.close();
                os.close();
                int responseCode = conn.getResponseCode();

                if (responseCode == HttpURLConnection.HTTP_OK) {
                    Log.i("response", "ok");
                    String line;
                    BufferedReader br=new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    while ((line=br.readLine()) != null) {
                        response.add(line);
                    }
                }else if(responseCode == 400){
                    Log.i("response code", "400");
                    return new String[]{"Error 400: BAD REQUEST"};
                } else {
                    return new String[]{"Error " + responseCode};
                }
            } catch (Exception e) {
                e.printStackTrace();
            }

            return response.toArray(new String[response.size()]);
        }

    }
}// end class ApiRequest
