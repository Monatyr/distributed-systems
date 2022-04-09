import com.rabbitmq.client.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public class Supplier extends RabbitClient{

        final String supplierName;
        String[] availableSupplies;

    public Supplier(String supplierName, String[] availableSupplies) throws IOException {
        super();
        this.supplierName = supplierName;
        this.availableSupplies = availableSupplies;

        for(String supplyName: availableSupplies){
            this.createAndBindQueue(this.getQueueName(supplyName), this.requirementsExchangeName, supplyName.toUpperCase());
            this.channel.basicConsume(this.getQueueName(supplyName), false, this.getSupplierConsumer());
        }

        this.createAndBindQueue(this.supplierName + "_ADMIN_QUEUE", this.adminExchangeName, "#.supplier");
        this.channel.basicConsume(this.supplierName + "_ADMIN_QUEUE", true, this.getAdminConsumer());
    }


    public Consumer getSupplierConsumer(){
        return new DefaultConsumer(channel){
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, "UTF-8");
                System.out.println(supplierName + " received: " + message);
                channel.basicAck(envelope.getDeliveryTag(), false);
            }
        };
    }


    public static void main(String args[]) throws IOException {
        System.out.println("Supplier created\n\nChoose available supplies:");
        for(Supplies supply: Supplies.values()){
            System.out.println("- " + supply.name());
        }

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String[] supplies = reader.readLine().split("\\s+");
        String supplierName = "";
        for(String s: supplies)
            supplierName += s.charAt(0);
        supplierName += "_SUPPLIER";
        System.out.println("Supplier's name: " + supplierName);

        Supplier supplier = new Supplier(supplierName, supplies);
    }
}
