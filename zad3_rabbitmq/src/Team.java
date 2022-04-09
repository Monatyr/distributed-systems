import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class Team extends RabbitClient{

    final String teamName;
    public static int teamCount = 0;

    public Team(String teamName) throws IOException {
        super();
        this.teamName = teamName;

        this.createAndBindQueue(this.teamName + "_ADMIN_QUEUE", this.adminExchangeName, "team.#");
        this.channel.basicConsume(this.teamName + "_ADMIN_QUEUE", true, this.getAdminConsumer());
    }


    public void run() throws IOException {
        System.out.println(this.teamName + " created\n");
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        Supplies[] suppliesNames = Supplies.values();

        while (true) {
            System.out.println("Choose needed supplies from a list below:");
            for(Supplies supplyName: suppliesNames)
                System.out.println("- " + supplyName);

            String[] supplies = reader.readLine().split("\\s+");
            for(String supplyName: supplies){
                String message = this.teamName + " requests '" + supplyName + "'";
                this.channel.basicPublish(this.requirementsExchangeName, supplyName.toUpperCase(), null, message.getBytes(StandardCharsets.UTF_8));
            }
        }
    }


    public static void main(String[] args) throws IOException {
        System.out.println("Input team's name: ");
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String teamName = reader.readLine();
        Team team = new Team(teamName);
//        Team team = new Team("TEAM_" + Integer.toString(1 + Team.teamCount++));
        team.run();
    }

}
