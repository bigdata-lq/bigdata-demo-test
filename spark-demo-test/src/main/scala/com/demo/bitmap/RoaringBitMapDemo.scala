package com.demo.bitmap

import org.roaringbitmap.RoaringBitmap

object RoaringBitMapDemo {

  def main(args: Array[String]): Unit = {
    val bitmap1: RoaringBitmap = RoaringBitmap.bitmapOf(1, 2, 3, 1000)
    val bitmap2: RoaringBitmap = new RoaringBitmap();
    bitmap2.add(4000, 4005);
    // 第三个数值，索引从0开始
    val thirdvalue: Int = bitmap1.select(3);
    // 2这个值的排序，排序索引从1开始，如果不在是0
    val indexoftwo: Int = bitmap1.rank(2)
    val c1 = bitmap1.contains(1000)
    val c2 = bitmap1.contains(7);

    println("bofore or, bitmap1 is: " + bitmap1);
    println("thirdvalue is: " + thirdvalue);
    println("indexoftwo is: " + indexoftwo);
    println("c1 is: " + c1);
    println("c2 is: " + c2);
    println();

    // 做并集
    val roaringBitmap = RoaringBitmap.or(bitmap1, bitmap2)

    println("bitmap1 is: " + bitmap1);
    println("bitmap2 is: " + bitmap2);
    println(roaringBitmap)


    val equals: Boolean = bitmap1.equals(bitmap2)
    println("is equals: " + equals);

    // 获取位图中元素个数
    val cardinality = bitmap1.getCardinality
    println("cardinality is: " + cardinality);


  }

}
