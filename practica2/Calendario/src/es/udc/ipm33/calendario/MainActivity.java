package es.udc.ipm33.calendario;

import java.util.Calendar;
import java.util.List;

import org.ektorp.CouchDbConnector;
import org.ektorp.DbAccessException;
import org.ektorp.android.util.EktorpAsyncTask;

import android.app.ProgressDialog;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.Menu;
import android.widget.Toast;

import com.roomorama.caldroid.CaldroidFragment;

import es.udc.ipm33.calendario.model.CouchDBAndroidHelper;
import es.udc.ipm33.calendario.model.EventDAO;
import es.udc.ipm33.calendario.model.EventVO;


public class MainActivity extends FragmentActivity {
	private CaldroidFragment caldroidFragment;
	private List<EventVO> events = null;
	private ProgressDialog progressDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Configure calendar view        
        caldroidFragment = new CaldroidFragment();
        Bundle args = new Bundle();
        Calendar cal = Calendar.getInstance();
        args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
        args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
        args.putInt(CaldroidFragment.START_DAY_OF_WEEK, CaldroidFragment.MONDAY);
        caldroidFragment.setArguments(args);

        FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.calendar1, caldroidFragment);
        t.commit();
        
        progressDialog = new ProgressDialog(MainActivity.this);
        progressDialog.setTitle(getString(R.string.loading));
        progressDialog.setMessage(getString(R.string.loading_events));
        progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER);
        progressDialog.show();
        
        // Get and mark event days
        EktorpAsyncTask getEventsTask = new EktorpAsyncTask() {

            @Override
            protected void doInBackground() {
                CouchDBAndroidHelper dbHelper = CouchDBAndroidHelper.getInstance();
                CouchDbConnector connector = dbHelper.getDbConnector();
                EventDAO eventDAO = new EventDAO(connector);
                events = eventDAO.getAll();
            }

            @Override
            protected void onSuccess() {
            	for (EventVO event:events) {
            		caldroidFragment.setBackgroundResourceForDate(R.color.blue, event.getDate());
            	}
            	progressDialog.dismiss();
            }

            @Override
            protected void onDbAccessException(DbAccessException dbAccessException) {
                Log.e("Calendar/MainActivity", "DbAccessException in background", dbAccessException);
                Toast.makeText(getApplicationContext(), "Error establishing a server connection!", Toast.LENGTH_LONG).show();
            }
        };
        getEventsTask.execute();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
    
}
