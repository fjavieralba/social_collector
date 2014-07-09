from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, KeyedProducer
import argparse
from social_collector import twitter, settings

def produce(broker_list, topic, keywords):
    tw = twitter.Twitter(**settings.twitter)
    kafka = KafkaClient(broker_list)

    #aynchronous producer that sends messages in batches
    producer = SimpleProducer(kafka, async=True, batch_send=True,
                              batch_send_every_n=10, batch_send_every_t=10)

	#send messages synchronously
    for raw_tweet in tw.stream(keywords):
		producer.send_messages(topic, raw_tweet)
		
    kafka.close()


#example:
#python bin/stream_to_kafka.py --broker-list localhost:9092 --topic twitter --keywords "produban,bancosantander,santander_es,santander_br,SantanderMx,santanderchile,FBBancoSantander,bsch,central hispano,banco santander,santanderGP,SacSantander_br,santanderukhelp,santanderuk,santanderpb,empleosantander"

if __name__ == "__main__":
    #parse args
    parser = argparse.ArgumentParser(description='Publish a realtime twitter stream into Kafka')
    parser.add_argument("--broker-list", dest="broker_list", help="comma separated list of kafka brokers", default=settings.kafka['broker_list'])
    parser.add_argument("--topic", dest="topic", help="kafka topic", default=settings.kafka['topic'])
    parser.add_argument('--keywords', dest="keywords", help='Keywords to use for filtering Twitter stream', nargs='+')

    args = parser.parse_args()

    produce(args.broker_list, args.topic, args.keywords)


