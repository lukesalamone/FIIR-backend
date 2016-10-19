package luke.com.fiirapp;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Spinner;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by luke on 10/18/16.
 */

public class SelectCarrierActivity extends Activity {

    Spinner spinner;
    Button button;

    String phone;
    String email;
    String invitedBy;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_carrier);
        Bundle extras = getIntent().getExtras();

        if(extras == null){
            Log.wtf("SelectCarrier", "extras is null!");
        } else {
            phone = extras.getString("phone");
            email = extras.getString("email");
            invitedBy = extras.getString("invitedBy");
        }

        spinner = (Spinner) findViewById(R.id.spinner);
        button = (Button) findViewById(R.id.button);
        button.setOnClickListener(this::onButtonClick);
    }

    void onButtonClick(View view){
        String carrier = String.valueOf(spinner.getSelectedItem());
        Log.i("selected carrier", carrier);
        carrier = parseCarrier(carrier);
        Log.i("parsed", carrier);

        // send carrier with post request
        try{
            ApiRequest api = new ApiRequest("http://fiirapp.ddns.net:9096");
            api.users_create(phone, invitedBy, email, carrier);
            String response = api.getResponse();
            JSONObject json = new JSONObject(response);
            if(json.getString("status").equals("ok")){
                // get userid and send to verify activity
                int userid = json.getInt("userid");

                Intent intent = new Intent(view.getContext(), VerifyActivity.class);
                intent.putExtra("userid", userid);

                startActivity(intent);

                if(android.os.Build.VERSION.SDK_INT >= 21) {
                    overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
                }
            } else {
                Log.wtf("users_create()", "returned error");
            }
        }catch (JSONException e){
            e.printStackTrace();
        }
    }

    private String parseCarrier(String carrier){
        switch (carrier){
            case "Alltel":
                return "alltel";
            case "AT & T":
                return "att";
            case "Boost Mobile":
                return "boost";
            case "Sprint":
                return "sprint";
            case "Virgin Mobile":
                return "virgin";
            case "US Cellular":
                return "uscellular";
            case "T-Mobile":
                return "tmobile";
            default:
                return "unknown";
        }
    }
}
