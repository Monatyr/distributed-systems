import com.rabbitmq.client.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

public class Admin extends RabbitClient{
    public static final String adminExchangeName = "ADMIN_EXCHANGE";

    Admin(Supplies[] allSupplies) throws IOException {
        super();

        this.createExchange(this.adminExchangeName, BuiltinExchangeType.TOPIC);

        for(Supplies supplyName: allSupplies){
            this.createAndBindQueue(this.getQueueName("ADMIN_" + supplyName.name()), this.requirementsExchangeName, supplyName.name().toUpperCase());
            this.channel.basicConsume(this.getQueueName("ADMIN_" + supplyName.name()), false, getConsumer());
        }
    }

    public Consumer getConsumer(){
        return new DefaultConsumer(channel){
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, "UTF-8");
                System.out.println("Admin received: " + message);
                channel.basicAck(envelope.getDeliveryTag(), false);
            }
        };
    }


    public static void main(String args[]) throws IOException, TimeoutException {
        Scanner scanner = new Scanner(System.in);
        Supplies[] supplies = Supplies.values();
        Admin admin = new Admin(supplies);
        System.out.println("Admin created");
        System.out.println("0 - quit\n1 - write to teams\n2 - write to suppliers\n3 - write to teams and suppliers");
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

        while(true){
            System.out.print("Choose message mode:\n");
            String queueKey = "quit";
            int mode = scanner.nextInt();

            switch(mode){
                case 0:
                    queueKey = "quit";
                    break;
                case 1:
                    queueKey = "team.#";
                    break;
                case 2:
                    queueKey = "#.supplier";
                    break;
                case 3:
                    queueKey = "team.supplier";
                    break;
            }

            if(queueKey.equals("quit")) {
                System.out.println("Admin closing");
                break;
            }

            System.out.print("Your message:\n");
            String message = reader.readLine();
            channel.basicPublish(adminExchangeName, queueKey, null, message.getBytes(StandardCharsets.UTF_8));
            System.out.println("Admin sent message with key '" + queueKey + "'");
        }
    }
}
