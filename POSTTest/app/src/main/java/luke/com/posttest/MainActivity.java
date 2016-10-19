package luke.com.posttest;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import org.json.JSONException;
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
import java.util.HashMap;
import java.util.Arrays;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    String TAG = "MainActivity";
    URL url;
    TextView textView;
    final String base = "http://fiirapp.ddns.net:9096";
    final String key = "DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS";
    final Integer userid = 1;
    PostFactory post;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = (TextView) findViewById(R.id.textView);
        post = new PostFactory(base);

        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
    }

    public void one(View view){
        textView.setText("sending...");
        try {
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("friend", new Integer(666));
            String response = post.performPostRequest("/users/setPromo", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void two(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            String response = post.performPostRequest("/pics/created", params);
            textView.setText(response);
        } catch(JSONException e){
            e.printStackTrace();
        }
    }
    public void three(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("picId", new Integer(1234));
            String response = post.performPostRequest("/pics/flag", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void four(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("picId", new Integer(1234));
            String response = post.performPostRequest("/pics/hide", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void five(View view){
        try{
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            String response = post.performPostRequest("/friends/list", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void six(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("friend", new Integer(987));
            String response = post.performPostRequest("/friends/add", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void seven(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("friend", new Integer(987));
            String response = post.performPostRequest("/friends/remove", params);
            textView.setText(response);
        }catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void eight(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("email", "test@test.com");
            String response = post.performPostRequest("/settings/update_email", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
    public void nine(View view){
        try {
            textView.setText("sending...");
            JSONObject params = new JSONObject();
            params.put("key", key);
            params.put("user", userid);
            params.put("phone", "1234567890");
            String response = post.performPostRequest("/settings/update_phone", params);
            textView.setText(response);
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
}
