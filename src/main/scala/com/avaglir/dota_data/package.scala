package com.avaglir

import skadistats.clarity.model.Entity
import skadistats.clarity.processor.runner.Context

import com.github.nscala_time.time.Imports._

package object dota_data {
  implicit class impEntity(v: Entity) {
    def isHero: Boolean = v.getDtClass.getDtName startsWith "CDOTA_Unit_Hero"
  }


  implicit class impContext(v: Context) {
    def tick = new Duration(v.getTick * 1000 / 30)
  }

  implicit class impDuration(v: Duration) {
    def clean: String = {
        (if (v.days > 0) s"${v.days}d" else "") +
        (if (v.hours % 24 > 0) s"${v.hours % 24}h" else "") +
        (if (v.minutes % 60 > 0) f"${v.minutes % 60}%02dm" else "") +
        (if (v.seconds % 60 > 0) f"${v.seconds % 60}%02ds" else "")
    }
  }
}
