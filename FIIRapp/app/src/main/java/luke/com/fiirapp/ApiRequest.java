package luke.com.fiirapp;

import android.os.AsyncTask;
import android.util.Log;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
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
import java.util.Iterator;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Created by luke on 10/5/16.
 *
 * Simple wrapper for sending POST requests to fiir API
 */

public class ApiRequest {
    private PostRequest post;
    private String key;
    private String userid;
    private String response;

    public ApiRequest(String url){
        this.post = new PostRequest(url);
    }

    public void setCredentials(String key, String userid){
        this.key = key;
        this.userid = userid;
        response = null;
    }
    public String getResponse(){
        String temp = this.response;
        this.response = null;
        return temp;
    }

    public void users_create(String phone, String invitedby, String email){
        JSONObject params = new JSONObject();
        try {
            params.put("phone", phone);
            params.put("invitedby", new Integer(invitedby));
            params.put("email", email);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/users/create", params));
    }
    public void users_create(String phone, String invitedby, String email, String carrier){
        JSONObject params = new JSONObject();
        try {
            params.put("phone", phone);
            params.put("invitedby", new Integer(invitedby));
            params.put("email", email);
            params.put("carrier", carrier);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/users/create", params));
    }
    public void users_login(String phone){
        try{
            JSONObject params = new JSONObject();
            params.put("phone", phone);
            response = Arrays.toString(post.execute("/users/login", params));
        } catch(JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
    }
    public void users_verify(int userid, String code){
        try {
            JSONObject params = new JSONObject();
            params.put("userid", new Integer(userid));
            params.put("code", new Integer(code));
            response = Arrays.toString(post.execute("/users/verify", params));
        } catch(JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
    }
    public void users_setPromo(String promoCode){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("promoCode", promoCode);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/users/setPromo", params));
    }
    public void pics_create(String filepath, String price, String token){
        if(token == null || token.length() == 0){
            token = this.key;
        }
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("file", filepath);
            params.put("price", new Integer(price));
            params.put("token", token);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/pics/create", params));
    }
    public void pics_created(){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/pics/created", params));
    }
    public void pics_flag(String pictureId){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("pictureId", new Integer(pictureId));
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("pics/flag", params));
    }
    public void pics_hide(String pictureId){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("pictureId", new Integer(pictureId));
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("pics/hide", params));
    }
    public void friends_list(){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("friends/list", params));
    }
    public void friends_add(String friendId){
        response = null;
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("friend", friendId);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("friends/add", params));
    }
    public void friends_remove(String friendId){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("friend", friendId);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("friends/remove", params));
    }
    public void settings_updateEmail(String email){
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("email", email);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("settings/update_email", params));
    }
    public void settings_updatePhone(String phone){
        response = null;
        JSONObject params = new JSONObject();
        try {
            params.put("key", key);
            params.put("user", new Integer(userid));
            params.put("phone", phone);
        } catch (JSONException e){
            e.printStackTrace();
            response = "JSON exception";
        }
        response = Arrays.toString(post.execute("/settings/update_phone", params));
    }

    /*
     * Handle transport of data over HTTP to various endpoints
     *
    */
    private class PostRequest{
        private String baseUrl;
        private URL url;
        public PostRequest(String baseUrl){
            this.baseUrl = baseUrl;
        }

        public String[] execute(String endpoint, JSONObject params) {
            ExecutorService executor = Executors.newSingleThreadExecutor();
            Callable<String[]> callable = new Callable<String[]>() {
                String[] result;

                @Override
                public String[] call() {
                    try {
                        url = new URL(baseUrl + endpoint);
                        Log.i("sending to url", url.toString());
                    } catch (MalformedURLException e) {
                        result = new String[]{"Malformed url: " + baseUrl + endpoint};
                    }

                    if(endpoint.equals("/pics/create")){
                        result = upload(params);
                    } else {
                        result = post(params);
                    }

                    return result;
                }
            };

            Future<String[]> future = executor.submit(callable);

            try {
                return future.get();
            }catch(Exception e){
                e.printStackTrace();
            }finally{
                executor.shutdown();
            }

            return new String[]{"exception thrown by Executor service"};
        }

        // post request with file upload and metadata
        private String[] upload(JSONObject params){
            String lineEnd = "\r\n";
            String twoHyphens = "--";
            int bytesRead, bytesAvailable, bufferSize;
            byte[] buffer;
            int maxBufferSize = 1*1024*1024;
            String boundary = Utils.getRandomString(15);
            ArrayList<String> response = new ArrayList<>();
            try {
                String filepath = (String)params.remove("file");
                String filename = filepath.substring(filepath.lastIndexOf('/') + 1);
                Log.i("filepath", filepath);
                Log.i("url", url.toString());
                FileInputStream fileInputStream = new FileInputStream(new File(filepath));
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();

                // Allow Inputs & Outputs.
                conn.setDoInput(true);
                conn.setDoOutput(true);
                conn.setUseCaches(false);

                // Set HTTP method to POST.
                conn.setRequestMethod("POST");

                conn.setRequestProperty("Connection", "Keep-Alive");
                conn.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);

                DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                //BufferedOutputStream os = new BufferedOutputStream(conn.getOutputStream());
                os.write((twoHyphens + boundary + lineEnd).getBytes("UTF-8"));
                os.write(("Content-Disposition: form-data; " +
                        "name=\"uploadedfile\";filename=\"" + filename + "\"" + lineEnd).getBytes("UTF-8"));
                os.write("Content-Type: image/jpeg\r\n".getBytes("UTF-8"));
                os.write(lineEnd.getBytes("UTF-8"));

                bytesAvailable = fileInputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);

                while (bytesRead > 0) {
                    os.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                }

                os.write(lineEnd.getBytes("UTF-8"));
                os.write((twoHyphens + boundary).getBytes("UTF-8"));

                // now add metadata
                Iterator<String> iterator = params.keys();
                while(iterator.hasNext()) {
                    String key = iterator.next();
                    String val = params.get(key).toString();

                    os.write(lineEnd.getBytes("UTF-8"));
                    os.write(("Content-Disposition: form-data; name=\"" + key + "\"").getBytes("UTF-8"));
                    os.write(lineEnd.getBytes("UTF-8"));
                    os.write(lineEnd.getBytes("UTF-8"));
                    os.write(val.getBytes("UTF-8"));
                    os.write(lineEnd.getBytes("UTF-8"));
                    os.write(twoHyphens.getBytes("UTF-8"));
                    os.write(boundary.getBytes("UTF-8"));
                }

                os.write(twoHyphens.getBytes("UTF-8"));
                os.write(lineEnd.getBytes("UTF-8"));

                response = handleResponse(conn);
                fileInputStream.close();

                os.flush();
                os.close();
            } catch(Exception e){
                e.printStackTrace();
            }

            return response.toArray(new String[response.size()]);
        }

        // post request with normal key-value pairs only
        private String[] post(JSONObject params){
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
                response = handleResponse(conn);
            } catch (Exception e) {
                e.printStackTrace();
            }

            return response.toArray(new String[response.size()]);
        }

        // handle server response
        private ArrayList<String> handleResponse(HttpURLConnection conn){
            ArrayList<String> response = new ArrayList<>();

            try {
                int responseCode = conn.getResponseCode();
                String line;
                BufferedReader br;

                if(responseCode >= 200 && responseCode <= 299){     // success
                    br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
                } else {
                    br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
                }

                while ((line=br.readLine()) != null) {
                    response.add(line);
                }

                return response;

            } catch(Exception e){
                e.printStackTrace();
            }

            response.add("Java IO Exception thrown");
            return response;
        }
    }// end PostRequest subclass
}// end class ApiRequest
