import com.rabbitmq.client.*;

import java.io.IOException;

public class RabbitClient {

    final String requirementsExchangeName = "REQUIREMENTS_EXCHANGE";
    final String adminExchangeName = "ADMIN_EXCHANGE";
    ConnectionFactory factory;
    Connection connection;
    static Channel channel;


    public RabbitClient() throws IOException {
        this.createChannel();
        this.createExchange(this.requirementsExchangeName, BuiltinExchangeType.DIRECT);
        this.createExchange(this.adminExchangeName, BuiltinExchangeType.TOPIC);
    }


    protected void createChannel(){
        this.factory = new ConnectionFactory();
        this.factory.setHost("localhost");
        try {
            this.connection = this.factory.newConnection();
            this.channel = this.connection.createChannel();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


    protected void createExchange(String exchangeName, BuiltinExchangeType type) throws IOException {
            this.channel.exchangeDeclare(exchangeName, type);
    }


    protected void createAndBindQueue(String queueName, String exchangeName, String queueKey) throws IOException {
        this.channel.queueDeclare(queueName, false, false, false, null);
        this.channel.queueBind(queueName, exchangeName, queueKey);
    }


    protected String getQueueName(String productName){
        return "QUEUE_" + productName.toUpperCase();
    }


    protected Consumer getAdminConsumer() {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, "UTF-8");
                System.out.println("Message from admin: " + message);
            }
        };
    }
}
