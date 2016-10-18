package luke.com.fiirapp;

import android.app.Activity;
import android.app.ActivityOptions;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;

/**
 * Created by luke on 10/17/16.
 */

public class LoadingActivity extends Activity{

    SharedPreferences preferences;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        Log.i("onCreate", "started loading activity");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Context context = getApplicationContext();
        preferences = PreferenceManager.getDefaultSharedPreferences(context);
        int userid = preferences.getInt("userid", -1);
        if(userid == -1){
            // go to login activity
            Intent intent = new Intent(this, LoginActivity.class);
            startActivity(intent);

            if(android.os.Build.VERSION.SDK_INT >= 21) {
                overridePendingTransition(R.anim.slide_in_right, android.R.anim.fade_out);
            }
        } else {
            // go to main activity
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
            if(android.os.Build.VERSION.SDK_INT >= 21) {
                overridePendingTransition(R.anim.gallery_slide_in, android.R.anim.fade_out);
            }
        }
    }
}
