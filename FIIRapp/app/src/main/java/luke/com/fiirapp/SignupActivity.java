package luke.com.fiirapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
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
    private String userid;

    private ApiRequest post;

    public SignupActivity(){
        post = new ApiRequest("http://fiirapp.ddns.net:9096");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

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

        if(!validPhone(phone)){
            showError("phone");
            valid = false;
        } else {
            resetMessage("phone");
        }
        if(!validEmail(email)){
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
                key = json.getString("key");
                userid = json.getString("userid");
                int verificationCode = json.getInt("code");

                // save key and userid to local storage

                // send verificationCode to VerifyActivity
                Intent intent = new Intent(view.getContext(), VerifyActivity.class);
                intent.putExtra("key_screen_name", verificationCode);
            }catch(JSONException e){
                // do nothing
            }
        }
    }

    private boolean validPhone(String phone){
        phone = phone.replace("-", "").replace("(", "").replace(")", "");
        return phone.length() == 9;
    }

    private boolean validEmail(String email){
        Pattern pattern = Pattern.compile("^[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6}$", Pattern.CASE_INSENSITIVE);
        Matcher matcher = pattern.matcher(email);
        return matcher.find();
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
