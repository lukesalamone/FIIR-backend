package luke.com.posttest;

import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by luke on 10/6/16.
 */

public class PostFactory {
    String baseUrl;
    URL url;
    public PostFactory(String baseUrl){
        this.baseUrl = baseUrl;
    }

    public String performPostRequest(String endpoint, JSONObject params){
        try {
            url = new URL(this.baseUrl + endpoint);
            Log.i("sending to url", url.toString());
        }catch(MalformedURLException e){
            return "{Malformed url: " + this.baseUrl + endpoint + "}";
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
                return "{Error: connection refused}";
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
                return "{Error 400: BAD REQUEST}";
            } else {
                return "{Error " + responseCode + "}";
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return Arrays.toString(response.toArray(new String[response.size()]));
    }
}
