# File with commands for manipulating the database
from ORM import models, manager, query


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    game_id = models.ForeignKeyField(Game, on_delete=models.OnDelete.NO_ACTION)


if __name__ == "__main__":
    Game.objects.create_table()
    Test.objects.create_table()
