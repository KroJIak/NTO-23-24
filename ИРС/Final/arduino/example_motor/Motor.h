#define FORWARD 1
#define RELEASE 0
#define BACKWARD -1

class Motor {
  public:
    Motor(int fPort, int bPort) {
      _fPort = fPort;
      _bPort = bPort;
      pinMode(_fPort, OUTPUT);
      pinMode(_bPort, OUTPUT);
    }
    void run(int direction) {
      switch (direction) {
        case FORWARD: {
          digitalWrite(_fPort, HIGH);
          digitalWrite(_bPort, LOW);
          break;
        } case RELEASE: {
          digitalWrite(_fPort, LOW);
          digitalWrite(_bPort, LOW);
          break;
        } case BACKWARD: {
          digitalWrite(_fPort, LOW);
          digitalWrite(_bPort, HIGH);
          break;
        }
      }
    }

  private:
    int _fPort;
    int _bPort;
};
