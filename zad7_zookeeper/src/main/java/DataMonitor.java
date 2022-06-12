import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;

import java.io.IOException;

public class DataMonitor implements Watcher {
	
	private final String znodePath;
	private final ZooKeeperApp mainApp;
	private final String execApp;
	private Process execAppProcess;
	private boolean externalAppRunning;
	
	public DataMonitor(ZooKeeperApp mainApp, String znodePath, String execApp) {
		this.mainApp = mainApp;
		this.znodePath = znodePath;
		this.execApp = execApp;
	}
	
	@Override
	public void process(WatchedEvent event) {
		if (event.getPath() == null) {
			return;
		}
		if (event.getPath().equals(this.znodePath)) {
			switch (event.getType()) {
				case NodeCreated -> {
					this.mainApp.setNodeExists(true);
					this.runApp();
				}
				case NodeDeleted -> {
					this.mainApp.setNodeExists(false);
					this.closeApp();
				}
			}
		} else if (event.getPath().startsWith(this.znodePath)) {
			Event.EventType eventType = event.getType();
			if (eventType.equals(Event.EventType.NodeCreated)|| eventType.equals(Event.EventType.NodeDeleted)) {
				countDescendants();
			}
		}
	}
	
	public void runApp() {
		try {
			System.out.println("Running " + this.execApp);
			this.execAppProcess = Runtime.getRuntime().exec(execApp);
			this.externalAppRunning = true;
		} catch (IOException e){
			e.printStackTrace();
		}
	}
	
	public void closeApp() {
		if (this.externalAppRunning) {
			System.out.println("Closing " + this.execApp);
			this.externalAppRunning = false;
			this.execAppProcess.destroy();
		}
	}

	public void countDescendants() {
		if (this.mainApp.getNodeExists()) {
			this.mainApp.getDescendantsNumber();
		}
	}
}
