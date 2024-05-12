#define E1  4 
#define M1 32
#define E2 19
#define M2 18
#define Mot_1_c1  12
#define Mot_1_c2  17
#define Mot_2_c1  14
#define Mot_2_c2  26

volatile int Mot_1_LastEncoded = 0;
volatile int Mot_1_EncoderValue = 0;
volatile int Mot_2_LastEncoded = 0;
volatile int Mot_2_EncoderValue = 0;

const int freq = 500;
const int ChannelE1 = 5;
const int ChannelE2 = 0;
const int resolution = 8;

void MoveForward(int dutyCycle)
{
  // Move Forward
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);
  
  ledcWrite(ChannelE1, dutyCycle);
  ledcWrite(ChannelE2, dutyCycle);
  return ;
}
void MoveBackward(int dutyCycle)
{
  // Move Backward
  digitalWrite(M1, HIGH);
  digitalWrite(M2, HIGH);
  
  ledcWrite(ChannelE1, dutyCycle);
  ledcWrite(ChannelE2, dutyCycle);
  return ;
}
void TurnLeft(int dutyCycle)
{
  // Turn left
  digitalWrite(M1, LOW);
  digitalWrite(M2, HIGH);
  
  ledcWrite(ChannelE1, dutyCycle);
  ledcWrite(ChannelE2, dutyCycle);
  return ;
}
void TurnRight(int dutyCycle)
{
  // Turn right
  digitalWrite(M1, HIGH);
  digitalWrite(M2, LOW);
  
  ledcWrite(ChannelE1, dutyCycle);
  ledcWrite(ChannelE2, dutyCycle);
  return ;
}
void Stop()
{
  int dutyCycle = 0;
  
  ledcWrite(ChannelE1, dutyCycle);
  ledcWrite(ChannelE2, dutyCycle);
  return ;
}
void SimpleMove()
{ 

  MoveForward(255);
  delay(5000);

  MoveBackward(255);
  delay(5000);

  TurnLeft(150);
  delay(1000);

  MoveForward(255);
  delay(5000);

  TurnRight(150);
  delay(1000);

  MoveBackward(255);
  delay(5000);

  Stop();
  delay(3000);

  return;
}
void ShowPowerControl()
{
  MoveForward(64);
  delay(3000);
  MoveForward(125);
  delay(3000);
  MoveForward(255);
  delay(3000);
  Stop();
  delay(1000);
}


void setup() {

  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);

  ledcSetup(ChannelE1, freq, resolution);
  ledcSetup(ChannelE2, freq, resolution);

  ledcAttachPin(E1, ChannelE1);
  ledcAttachPin(E2, ChannelE2);

  Serial.begin(115200);
  
  pinMode(Mot_1_c1, INPUT_PULLUP);
  pinMode(Mot_1_c2, INPUT_PULLUP);
  pinMode(Mot_2_c1, INPUT_PULLUP);
  pinMode(Mot_2_c2, INPUT_PULLUP);

  digitalWrite(Mot_1_c1, HIGH);
  digitalWrite(Mot_1_c2, HIGH);
  digitalWrite(Mot_2_c1, HIGH);
  digitalWrite(Mot_2_c2, HIGH);

  attachInterrupt(Mot_1_c2, Mot_1_UpdateEncoder, CHANGE);
  attachInterrupt(Mot_1_c1, Mot_1_UpdateEncoder, CHANGE);

  
  attachInterrupt(Mot_2_c2, Mot_2_UpdateEncoder, CHANGE);
  attachInterrupt(Mot_2_c1, Mot_2_UpdateEncoder, CHANGE);
  
}

void loop() 
{
  //SimpleMove();

  //ShowPowerControl();

/*  MoveForward(255);
  for (int i = 0; i < 50 ; i ++ )
  {
    Serial.println(Mot_1_EncoderValue);
    delay(100);
  }
  
  Stop();
  delay(2000); */

   MoveBackward(255);
  for (int i = 0; i < 50 ; i ++ )
  {
    Serial.println(Mot_1_EncoderValue);
    delay(100);
  }
  
  Stop();
  delay(2000); 
    
  
}

void Mot_1_UpdateEncoder()
{
  int MSB = digitalRead(Mot_1_c1);
  int LSB = digitalRead(Mot_1_c2);

  int encoded = (MSB << 1) | LSB;
  int sum = (Mot_1_LastEncoded << 2) | encoded;

  if ( (sum == 0b1101) || (sum == 0b0100) || (sum == 0b0010) || (sum == 0b1011) )
    Mot_1_EncoderValue--;
  if ( (sum == 0b1110) || (sum == 0b0111) || (sum == 0b0001) || (sum == 0b1000) )
    Mot_1_EncoderValue++;

  Mot_1_LastEncoded = encoded;
  
}

void Mot_2_UpdateEncoder()
{
  int MSB = digitalRead(Mot_2_c1);
  int LSB = digitalRead(Mot_2_c2);

  int encoded = (MSB << 1) | LSB;
  int sum = (Mot_2_LastEncoded << 2) | encoded;

  if ( (sum == 0b1101) || (sum == 0b0100) || (sum == 0b0010) || (sum == 0b1011) )
    Mot_2_EncoderValue--;
  if ( (sum == 0b1110) || (sum == 0b0111) || (sum == 0b0001) || (sum == 0b1000) )
    Mot_2_EncoderValue++;

  Mot_2_LastEncoded = encoded;
  
}
