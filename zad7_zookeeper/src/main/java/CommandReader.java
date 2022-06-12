import java.io.*;
import java.net.ConnectException;
import java.nio.channels.ClosedChannelException;

public class CommandReader implements Runnable {
	
	private final BufferedReader bufferedReader;
	private final ZooKeeperApp mainApp;
	private boolean flag = true;
	
	public CommandReader(ZooKeeperApp zooKeeperApp) {
		this.mainApp = zooKeeperApp;
		this.bufferedReader = new BufferedReader(new InputStreamReader(System.in));
	}
	
	@Override
	public void run() {
		while (flag) {
			try {
				String line = this.bufferedReader.readLine();
				if (line.equals("tree")) {
					this.mainApp.showTreeStructure();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void exit() {
		this.flag = false;
		try {
			this.bufferedReader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
