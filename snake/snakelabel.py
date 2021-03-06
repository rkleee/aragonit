import numpy
from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class SnakeLabel(qw.QLabel):

    def __init__(self, width, height):
        super(SnakeLabel, self).__init__()
        self.setWindowTitle("Snake")

        # size of the playing field in pixel
        # one pixel = one block for the snake
        self.width = width
        self.height = height
        # automatically scales the playing field according
        # to the size of the parent container
        self.setScaledContents(True)

        # creates timer to keep the snake moving
        self.timer = qc.QTimer()
        self.timer.timeout.connect(self.moveSnake)

        # uses a semaphore to avoid multiple threads changing
        # the direction simultanously
        self.isChangingDirection = False

        # indicates if the game is running or not
        self.isRunning = False

        # sets default speed value
        #
        # integer between 1 and 20 indicating the actual speed
        # 1 = very slow
        # 20 = very fast
        self.setSpeed(5)

        # indicates how many points are necessary to increase the speed
        self.points_to_speed_increase = 3
        # current score since the last speed increase
        self.points_since_speed_increase = 0
        # overall score
        self.score = 0

        # sets colours for different items
        self.snake_color = 0x00000000
        self.background_color = 0xffffffff
        self.fruit_color = 0x00FF0000

        # initializes the playing field
        self.playing_field = qg.QImage(width, height, qg.QImage.Format_RGB32)
        self.playing_field.fill(self.background_color)

        # creates the snake in the lower left corner
        #
        # first tuple in the list represents the first
        # snake element concerning the moving direction
        self.snake_position = [
            [3, self.height - 1],
            [2, self.height - 1],
            [1, self.height - 1],
            [0, self.height - 1]
        ]
        # draws the initially created snake
        for pos in self.snake_position:
            self.playing_field.setPixel(pos[0], pos[1], self.snake_color)
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

        # initially, snake moves to the right
        self.direction = 1

        # variable to store the fruit's location
        self.fruit_coordinate = [0, 0]

        self.drawFruit()

        self.show()

    def moveSnake(self):
        # gets beginning of snake
        x_value = self.snake_position[0][0]
        y_value = self.snake_position[0][1]

        # calculates new beginning of snake
        if (self.direction == 0):
            y_value = y_value - 1
        elif (self.direction == 1):
            x_value = x_value + 1
        elif (self.direction == 2):
            y_value = y_value + 1
        elif (self.direction == 3):
            x_value = x_value - 1

        # only draws the snake if its new beginning is valid
        crossedBorder = self.crossedBorder(x_value, y_value)
        pushedSnake = self.pushedSnake(x_value, y_value)
        if not crossedBorder and not pushedSnake:
            self.playing_field.setPixel(
                x_value, y_value, self.snake_color)
            self.snake_position.insert(0, [x_value, y_value])
            self.setPixmap(qg.QPixmap.fromImage(self.playing_field))
            # resets the semaphore after drawing the snake
            self.isChangingDirection = False
        else:
            self.stopGame()

        # gets and deletes the end of the snake only
        # if it does not push a fruit
        if not self.pushedFruit(x_value, y_value):
            x_value = self.snake_position[-1][0]
            y_value = self.snake_position[-1][1]
            self.playing_field.setPixel(
                x_value, y_value, self.background_color)
            del(self.snake_position[-1])
        else:
            self.points_since_speed_increase += 1
            self.score += 1

            # increases speed when necessary
            if self.points_since_speed_increase >= self.points_to_speed_increase:
                self.increaseSpeed()

            self.drawFruit()

    def crossedBorder(self, x, y):
        """Return true if given coordinates are outside the playing field."""
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def pushedSnake(self, x, y):
        """Return true if coordinates are part of the snake."""
        pushedSnake = False
        for pos in self.snake_position:
            if pos[0] == x and pos[1] == y:
                pushedSnake = True
                break
        return pushedSnake

    def pushedFruit(self, x, y):
        """Return true if coordinates point to the fruit."""
        return self.fruit_coordinate[0] == x and self.fruit_coordinate[1] == y

    def drawFruit(self):
        """
        Choose the position of the fruit randomly.

        Only draws the fruit if its position is valid.
        """
        # TODO: create better function to generate a new fruit position
        #
        # at the moment, the function may run endlessly if the snake is very
        # long
        valid_fruit = False
        while not valid_fruit:
            fruit_x_value = numpy.random.randint(0, self.width)
            fruit_y_value = numpy.random.randint(0, self.height)
            if not self.pushedSnake(fruit_x_value, fruit_y_value):
                valid_fruit = True
        self.fruit_coordinate = [fruit_x_value, fruit_y_value]
        self.playing_field.setPixel(
            fruit_x_value, fruit_y_value, self.fruit_color)
        self.setPixmap(qg.QPixmap.fromImage(self.playing_field))

    def keyPressEvent(self, event):
        """
        Translate the pressed arrow key into an integer.

        Stores the last pressed key in its integer representation
        into the "direction" variable. Only allows direction changes
        to the right or to the left relative to the actual moving direction.

        Up = 0
        Right = 1
        Down = 2
        Left = 3

        Uses the 'P' key to pause or restart the game.
        """
        # uses the arrow keys to control the snake
        #
        # changing the direction is only allowed if last change
        # is already drawn
        if not self.isChangingDirection:
            if event.key() == qc.Qt.Key_Up and self.direction != 2:
                self.direction = 0
            elif event.key() == qc.Qt.Key_Right and self.direction != 3:
                self.direction = 1
            elif event.key() == qc.Qt.Key_Down and self.direction != 0:
                self.direction = 2
            elif event.key() == qc.Qt.Key_Left and self.direction != 1:
                self.direction = 3
            # sets the semaphore which locks further direction changes
            self.isChangingDirection = True
        # uses the 'p' key to pause or restart the game
        if event.key() == qc.Qt.Key_P:
            if self.isRunning:
                self.pauseGame()
            else:
                self.startGame()

    def calcSpeed(self, speed):
        """
        Calculate the actual timer interval (in milliseconds).

        Uses the given speed attribute as base of the calculation.
        """
        return 1000 / speed

    def setSpeed(self, speed):
        self.speed = speed
        self.timer.setInterval(self.calcSpeed(speed))

    def increaseSpeed(self):
        if self.speed < 20:
            self.speed += 1
            self.setSpeed(self.speed)

    def startGame(self):
        self.isRunning = True
        self.timer.start()

    def pauseGame(self):
        self.isRunning = False
        self.timer.stop()

    def stopGame(self):
        self.isRunning = False
        self.timer.stop()
        self.parent().showResult(self.score)
