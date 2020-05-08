# How to recalculate MySQL ITEM IDs
Did you get the "ItemIDRange: NO MORE ITEM ID RANGE" error?

There are many ways to fix this.

My suggestion is to recalculate the mysql player.item.id field. There are two ways to do so.

1. deleting and recreate `id` but losing the insert order

	```sql
	ALTER TABLE `item` DROP `id`;
	ALTER TABLE `item` AUTO_INCREMENT = 10000001;
	ALTER TABLE `item` ADD `id` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;
	```

2. update the `id` and keeping the previous insert order

	```sql
	SET @id:=10000000;
	UPDATE `item` SET id=@id:=@id+1 ORDER BY id;
	ALTER TABLE `item` AUTO_INCREMENT = 0;
	```

_Note: Both of them will have new `id`s so you can't track them from the old log.log anymore._
