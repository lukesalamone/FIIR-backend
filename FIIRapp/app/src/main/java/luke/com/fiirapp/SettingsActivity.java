package luke.com.fiirapp;

import android.app.Activity;
import android.app.ActivityOptions;
import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.support.v4.view.GestureDetectorCompat;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;
import android.widget.RelativeLayout;
import android.widget.TextView;

/**
 * Created by luke on 4/19/16.
 */
public class SettingsActivity extends Activity {

    RelativeLayout settingsBG;
    TextView title;
    GestureDetectorCompat detector;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.settings);

        settingsBG = (RelativeLayout) findViewById(R.id.settings_bg);
        title = (TextView) findViewById(R.id.settings_title);
        title.setTypeface(Typeface.createFromAsset(getAssets(),"hnt.ttf"));

        detector = new GestureDetectorCompat(this, new gestureListener());
    }

    @Override
    public boolean onTouchEvent(MotionEvent event){
        detector.onTouchEvent(event);
        return super.onTouchEvent(event);
    }

    void openGallery(){
        Intent intent = new Intent(this, MainActivity.class);
        if(android.os.Build.VERSION.SDK_INT >= 21) {
            startActivity(intent,
                    ActivityOptions.makeSceneTransitionAnimation(this).toBundle());
            overridePendingTransition(R.anim.gallery_slide_in, android.R.anim.fade_out);
        }else{
            startActivity(intent);
        }
    }

    class gestureListener extends GestureDetector.SimpleOnGestureListener {
        private static final String DEBUG_TAG = "Gestures";

        @Override
        public boolean onDown(MotionEvent event) {
            return true;
        }

        @Override
        public boolean onFling(MotionEvent event1, MotionEvent event2, float velocityX, float velocityY) {
            if(Math.abs(velocityX) > Math.abs(velocityY)){
                if(velocityX > 0){ // fling right
                    // do nothing
                }else{
                    openGallery();
                }
            }

            return true;
        }// end onFling method
    }// end of gestureListener subclass
}
