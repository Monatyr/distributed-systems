import org.apache.zookeeper.AddWatchMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooKeeper;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.stream.Stream;

public class ZooKeeperApp{
	
	private final ZooKeeper zooKeeper;
	private final DataMonitor dataMonitor;
	private final String znodePath;
	private final CommandReader commandReader;
	private boolean nodeExists;
	private Thread commandReaderThread;
	
	
	public ZooKeeperApp(String hostNames, String znodePath, String execAppPath) throws IOException {
		this.znodePath = znodePath;
		this.commandReader = new CommandReader(this);
		this.dataMonitor = new DataMonitor(this, znodePath, execAppPath);
		this.zooKeeper = new ZooKeeper(hostNames, 3000, this.dataMonitor);
		this.addWatchToNode(znodePath, AddWatchMode.PERSISTENT_RECURSIVE);
		this.commandReaderThread = new Thread(this.commandReader);
		this.commandReaderThread.start();
	}
	
	public void addWatchToNode(String nodePath, AddWatchMode watchMode) {
		try {
			this.zooKeeper.addWatch(nodePath, watchMode);
		} catch (KeeperException e) {
			System.out.println("[ConnectionLoss] Can't connect to server");
			this.commandReader.exit();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void getDescendantsNumber() {
		try {
			if (nodeExists)
				System.out.println("Number of descendants of node " + this.znodePath + ": "
						+ this.zooKeeper.getAllChildrenNumber(znodePath));
		} catch (KeeperException ignored) {
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void showTreeStructure() {
		System.out.print("Tree structure of node " + this.znodePath + ": ");
		Stream.of(getDescendants()).forEach(System.out::println);
	}
	
	public List<String> getDescendants() {
		try {
			ArrayList<String> descendants = new ArrayList<>();
			if (nodeExists) {
				String currNode = "";
				Stack<String> bfsStack = new Stack<>();
				bfsStack.push(this.znodePath);
				while (!bfsStack.empty()) {
					currNode = bfsStack.pop();
					for (String childNode : this.zooKeeper.getChildren(currNode, true)) {
						String childNodePath = String.join("/", currNode, childNode);
						descendants.add(childNodePath);
						bfsStack.add(childNodePath);
					}
				}
			}
			return descendants;
		} catch (KeeperException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	public void setNodeExists(boolean nodeExists) {
		this.nodeExists = nodeExists;
	}
	
	public boolean getNodeExists() {
		return nodeExists;
	}
}
