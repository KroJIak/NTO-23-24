#define FORWARD 0
#define BACKWARD 1

class Motor {
  public:
    Motor(int _dPort, int _sPort, int _e1Port, int _e2Port, int _channelEncoder) {
      dPort = _dPort;
      sPort = _sPort;
      e1Port = _e1Port;
      e2Port = _e2Port;
      channelEncoder = _channelEncoder;

      pinMode(dPort, OUTPUT);
      ledcSetup(channelEncoder, freq, resolution);
      ledcAttachPin(sPort, channelEncoder);
      pinMode(e1Port, INPUT_PULLUP);
      pinMode(e2Port, INPUT_PULLUP);
      digitalWrite(e1Port, HIGH);
      digitalWrite(e2Port, HIGH);
    }

    void updateEncoder() {
      int MSB = digitalRead(e1Port);
      int LSB = digitalRead(e2Port);
      int encoded = (MSB << 1) | LSB;
      int sum = (lastEncoded << 2) | encoded;
      if ((sum == 0b1101) || (sum == 0b0100) || (sum == 0b0010) || (sum == 0b1011))
        encoder--;
      if ((sum == 0b1110) || (sum == 0b0111) || (sum == 0b0001) || (sum == 0b1000))
        encoder++;
      lastEncoded = encoded;
    }

    int getEncoder() {
      return encoder - lastEncoder;
    }

    void resetEncoder() {
      lastEncoder = encoder;
    }

    void run(int direction) {
      digitalWrite(dPort, direction);
    }

    void setSpeed(int speed) { // speed: 0-255
      ledcWrite(channelEncoder, speed);
    }

  private:
    int dPort;
    int sPort;
    int e1Port;
    int e2Port;
    volatile int lastEncoded = 0;
    volatile int encoder = 0;
    int lastEncoder = 0;
    int channelEncoder;
    const int freq = 500;
    const int resolution = 8;
};
