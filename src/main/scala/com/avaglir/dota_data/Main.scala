package com.avaglir.dota_data

import java.io.{BufferedWriter, File, FileWriter}

import skadistats.clarity.event.Event
import skadistats.clarity.model.s2.S2CombatLogEntry
import skadistats.clarity.model.{CombatLogEntry, Entity, FieldPath, GameEvent}
import skadistats.clarity.processor.entities.{OnEntityCreated, OnEntityUpdated, UsesEntities}
import skadistats.clarity.processor.gameevents.{OnCombatLogEntry, OnGameEvent}
import skadistats.clarity.processor.reader.OnMessage
import skadistats.clarity.processor.runner.{Context, ControllableRunner, SimpleRunner}
import skadistats.clarity.source.MappedFileSource
import skadistats.clarity.wire.common.proto.DotaUserMessages
import skadistats.clarity.wire.s2.proto.S2UserMessages
import skadistats.clarity.wire.s2.proto.S2UserMessages._

object Main {
  val source = new MappedFileSource("replays/2460435158.dem")
  val runner = new SimpleRunner(source)

  var ticking = 10

  def main(args: Array[String]): Unit = {
    val proc = new ClarityTest
    runner runWith proc
//    runner seek runner.getLastTick

//    while (ticking > 0 && !runner.isAtEnd) {
//      runner.tick()
//    }

//    runner seek runner.getLastTick

    proc.outfile.close()
  }
}

@UsesEntities
class ClarityTest {
  val outfile = new BufferedWriter(new FileWriter(new File("out")))

//  @OnEntityUpdated
//  def onUpdated(context: Context, entity: Entity, fieldPath: Array[FieldPath], updateCount: Int): Unit = {
//    if (!entity.isHero) return
//    println(entity)
//    Main.ticking = false
//
//    val g = entity.getProperty[Int]("")
//    println(s"hero ${entity.getDtClass.getDtName} gold $g")
//  }

//  @OnGameEvent
//  def onGameEvent(context: Context, event: GameEvent): Unit = {
//    println(event)
//    event.
//    Main.ticking -= 1
//  }



//  @OnMessage(classOf[DotaUserMessages.])
//  def onMessage(context: Context, message: CUserMessageSayText2): Unit = {
//    outfile write s"$message\n"
//
//    Main.ticking -= 1
//  }

  @OnCombatLogEntry
  def onCombatLogEntry(context: Context, cle: S2CombatLogEntry): Unit = {
    if (cle.getTargetName != "npc_dota_hero_medusa") return

    if (cle.getObsWardsPlaced == 1) {
//      outfile write s"${cle.getTargetName}\n"
      outfile write s"$cle"
//      outfile write s"$cle\n"
    }
  }
}
