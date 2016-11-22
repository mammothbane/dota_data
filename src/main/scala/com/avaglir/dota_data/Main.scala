package com.avaglir.dota_data

import skadistats.clarity.model.{Entity, FieldPath}
import skadistats.clarity.processor.entities.{OnEntityCreated, OnEntityUpdated}
import skadistats.clarity.processor.runner.{Context, SimpleRunner}
import skadistats.clarity.source.MappedFileSource

object Main {
  def main(args: Array[String]): Unit = {
    val proc = new ClarityTest

    new SimpleRunner(new MappedFileSource("replays/2460435158.dem")) runWith proc
    println(proc.creationCount)
  }
}

class ClarityTest {
  var creationCount = 0

  @OnEntityCreated
  def onCreated(context: Context, entity: Entity): Unit = {
    if (!entity.isHero) return

    println(s"hero created at ${context.tick.clean}")
  }

  @OnEntityUpdated
  def onUpdated(context: Context, entity: Entity, fieldPath: Array[FieldPath], updateCount: Int): Unit = {
    if (!entity.isHero) return
    println(s"processing hero update at ${context.tick.clean}")
  }
}
