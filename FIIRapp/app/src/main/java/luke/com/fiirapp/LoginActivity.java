package luke.com.fiirapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by luke on 10/17/16.
 */

public class LoginActivity extends Activity {

    Button login;
    Button register;
    EditText numberField;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Log.i("onCreate", "started login activity");

        login = (Button) findViewById(R.id.login);
        register = (Button) findViewById(R.id.register);
        numberField = (EditText) findViewById(R.id.phone_input);

        login.setOnClickListener(this::login);
        register.setOnClickListener(this::register);
    }

    // send phone number from text field to verify activity
    void login(View view){
        String phone = numberField.getText().toString();

        if(!Utils.validPhone(phone)){
            // TODO create toast
            return;
        }

        ApiRequest api = new ApiRequest("http://fiirapp.ddns.net:9096");
        api.users_login(phone);
        String response = api.getResponse();
        try{
            JSONObject json = new JSONObject(response);
            if(!json.getString("status").equals("ok")){
                // TODO create toast
                return;
            }
            int userid = json.getInt("message");

            // go to verify activity
            Intent intent = new Intent(this, VerifyActivity.class);
            intent.putExtra("userid", userid);
            startActivity(intent);

            if(android.os.Build.VERSION.SDK_INT >= 21) {
                overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
            }
        }catch (JSONException e){
            e.printStackTrace();
        }
    }

    // go to signup activity
    void register(View view){
        Intent intent = new Intent(this, SignupActivity.class);
        startActivity(intent);

        if(android.os.Build.VERSION.SDK_INT >= 21) {
            overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
        }
    }
}
