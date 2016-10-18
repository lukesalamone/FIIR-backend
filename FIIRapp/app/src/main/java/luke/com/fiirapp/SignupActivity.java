package luke.com.fiirapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by luke on 10/11/16.
 */

public class SignupActivity extends Activity {

    Button button;
    EditText phoneInput;
    EditText emailInput;
    EditText inviteInput;
    TextView phoneLabel;
    TextView emailLabel;
    TextView inviteLabel;

    private String key;
    private int userid;

    private ApiRequest post;

    public SignupActivity(){
        post = new ApiRequest("http://fiirapp.ddns.net:9096");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        Log.i("onCreate", "started signup activity");

        button = (Button) findViewById(R.id.button);
        phoneInput = (EditText) findViewById(R.id.phone_input);
        emailInput = (EditText) findViewById(R.id.email_input);
        inviteInput = (EditText) findViewById(R.id.invited_input);
        phoneLabel = (TextView) findViewById(R.id.phone_label);
        emailLabel = (TextView) findViewById(R.id.email_label);
        inviteLabel = (TextView) findViewById(R.id.invited_label);

        button.setOnClickListener(this::onSignupButtonClicked);
    }

    void onSignupButtonClicked(View view){
        String phone;
        String invitedby;
        String email;
        boolean valid = true;

        // check input fields are populated
        phone = phoneInput.getText().toString();
        email = emailInput.getText().toString();
        invitedby = inviteInput.getText().toString();

        if(!Utils.validPhone(phone)){
            showError("phone");
            valid = false;
        } else {
            resetMessage("phone");
        }
        if(!Utils.validEmail(email)){
            showError("email");
            valid = false;
        } else {
            resetMessage("email");
        }
        if(!validInvite(invitedby)){
            showError("invite");
            valid = false;
        } else {
            resetMessage("invite");
        }

        // fire post request to /users/create
        if(valid) {
            try {
                post.users_create(phone, invitedby, email);
                String response = post.getResponse();
                JSONObject json = new JSONObject(response);
                userid = json.getInt("userid");

                // send userid to VerifyActivity
                Intent intent = new Intent(view.getContext(), VerifyActivity.class);
                intent.putExtra("userid", userid);

                startActivity(intent);

                if(android.os.Build.VERSION.SDK_INT >= 21) {
                    overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
                }
            }catch(JSONException e){
                // do nothing
            }
        }
    }



    // TODO use api request
    private boolean validInvite(String invite){
        return true;
    }

    private void showError(String target){
        switch (target){
            case "phone":
                phoneLabel.setText("invalid number");
                break;
            case "email":
                emailLabel.setText("invalid email");
                break;
            case "invite":
                inviteLabel.setText("invalid invite token");
                break;
        }
    }

    private void resetMessage(String target){
        switch (target){
            case "phone":
                phoneLabel.setText("phone number");
                break;
            case "email":
                emailLabel.setText("email address");
                break;
            case "invite":
                inviteLabel.setText("invited by (optional)");
                break;
        }
    }
}// end SignupActivity class
