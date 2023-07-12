package com.demo.bitmap

import org.roaringbitmap.RoaringBitmap

import java.io.{ByteArrayInputStream, ByteArrayOutputStream, DataInputStream, DataOutputStream}

object BitmapUtil {
  /**
   * 序列化bitmap
   */
  def serBitmap(bm: RoaringBitmap): Array[Byte] = {
    val stream = new ByteArrayOutputStream()
    val dataOutput = new DataOutputStream(stream)
    bm.serialize(dataOutput)
    stream.toByteArray
  }

  /**
   * 反序列bitmap
   */
  def deSerBitmap(bytes: Array[Byte]): RoaringBitmap = {
    val bm: RoaringBitmap = RoaringBitmap.bitmapOf()
    val stream = new ByteArrayInputStream(bytes)
    val inputStream = new DataInputStream(stream)
    bm.deserialize(inputStream)
    bm
  }
}
