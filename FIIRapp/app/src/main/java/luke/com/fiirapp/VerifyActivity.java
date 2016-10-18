package luke.com.fiirapp;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by luke on 10/12/16.
 */

public class VerifyActivity extends Activity {

    private EditText codeField;
    private Button button;
    private SharedPreferences preferences;
    private int userid;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_verify);

        codeField = (EditText) findViewById(R.id.code);
        preferences = getPreferences(MODE_PRIVATE);
        Bundle extras = getIntent().getExtras();
        userid = (extras == null) ? -1 : extras.getInt("key_userid");

        Log.wtf("verifyActivity", "extras was null!");

        button = (Button) findViewById(R.id.button);
        button.setOnClickListener(this::verifyCode);
        disableButton();

        codeField.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if(s.length() == 6){
                    for(int i=0; i<6; i++){
                        if(!Character.isDigit(s.charAt(i))){
                            disableButton();
                            return;
                        }
                    }
                    enableButton();
                }
            }

            @Override
            public void afterTextChanged(Editable s) {

            }
        });
    }

    void enableButton(){
        // TODO add cool gui cue
        button.setEnabled(true);
    }

    void disableButton(){
        // TODO add gui cue
        button.setEnabled(false);
    }

    void verifyCode(View view){
        String verificationCode = codeField.getText().toString();

        ApiRequest api = new ApiRequest("http://fiirapp.ddns.net:9096");
        api.users_verify(userid, verificationCode);
        try{
            JSONObject json = new JSONObject(api.getResponse());
            if(json.getString("status").equals("ok")){
                String key = json.getString("message");
                SharedPreferences.Editor editor = preferences.edit();
                editor.putInt("userid", userid);
                editor.putString("key", key);
                editor.apply();

                Log.i("verifyCode", "key saved as " + preferences.getString("key", ""));
            }
        } catch (JSONException e){
            e.printStackTrace();
        }
    }
}
