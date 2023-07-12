package com.demo.bitmap

import org.apache.spark.sql.{Encoder, Encoders}
import org.apache.spark.sql.expressions.Aggregator
import org.roaringbitmap.RoaringBitmap


class BitmapOrMergeUDAF extends Aggregator[Array[Byte], Array[Byte], Array[Byte]] {
  override def zero: Array[Byte] = {
    val bitmap: RoaringBitmap = RoaringBitmap.bitmapOf()
    BitmapUtil.serBitmap(bitmap)
  }

  override def reduce(b: Array[Byte], a: Array[Byte]): Array[Byte] = {
    val bitmap1: RoaringBitmap = BitmapUtil.deSerBitmap(b)
    val bitmap2: RoaringBitmap = BitmapUtil.deSerBitmap(a)
    bitmap1.or(bitmap2)
    BitmapUtil.serBitmap(bitmap1)
  }

  override def merge(b1: Array[Byte], b2: Array[Byte]): Array[Byte] = {
    val bitmap1: RoaringBitmap = BitmapUtil.deSerBitmap(b1)
    val bitmap2: RoaringBitmap = BitmapUtil.deSerBitmap(b2)
    bitmap1.or(bitmap2)
    BitmapUtil.serBitmap(bitmap1)
  }

  override def finish(reduction: Array[Byte]): Array[Byte] = reduction

  override def bufferEncoder: Encoder[Array[Byte]] = Encoders.BINARY

  override def outputEncoder: Encoder[Array[Byte]] = Encoders.BINARY
}
