import org.jetbrains.annotations.NotNull;

import java.io.IOException;

public class Main {
	
	public static void main(@NotNull String[] args) {
		String hostNames = args[0];
		String znodePath = args[1];
		String execAppPath = args[2];
		
		try {
			ZooKeeperApp mainApp = new ZooKeeperApp(hostNames, znodePath, execAppPath);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
