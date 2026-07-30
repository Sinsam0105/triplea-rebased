package games.strategy.triplea.delegate;

import com.google.common.annotations.VisibleForTesting;
import games.strategy.engine.data.GameData;
import games.strategy.engine.data.Unit;
import games.strategy.triplea.attachments.UnitAttachment;
import games.strategy.triplea.delegate.supply.SupplyNetworkResolver;
import lombok.experimental.UtilityClass;

/** Resolves a unit's maximum movement for the current movement phase. */
@UtilityClass
public final class MovementAllowanceResolver {
  /**
   * Movement a land unit keeps while out of supply. It may still shuffle one border (a breakout or
   * a fighting withdrawal) but cannot redeploy or blitz: a blitz needs at least two movement to
   * pass through and continue, which this cap forbids on its own.
   */
  private static final int OUT_OF_SUPPLY_MOVEMENT = 1;

  public enum MovementPhase {
    COMBAT,
    REDEPLOYMENT,
    OTHER
  }

  public static int resolveMaximumMovement(final Unit unit) {
    return resolveMaximumMovement(unit, resolveCurrentPhase(unit.getData()));
  }

  @VisibleForTesting
  public static int resolveMaximumMovement(final Unit unit, final MovementPhase phase) {
    final UnitAttachment attachment = unit.getUnitAttachment();
    final int attachmentMovement =
        switch (phase) {
          case COMBAT -> attachment.getCombatMovement(unit.getOwner());
          case REDEPLOYMENT -> attachment.getRedeploymentMovement(unit.getOwner());
          case OTHER -> attachment.getMovement(unit.getOwner());
        };
    final int movement = Math.max(0, attachmentMovement + unit.getBonusMovement());
    if (SupplyNetworkResolver.isOutOfSupply(unit, unit.getData())) {
      // Redeployment (afmov) is forbidden entirely; combat and other moves keep a single step.
      return phase == MovementPhase.REDEPLOYMENT ? 0 : Math.min(movement, OUT_OF_SUPPLY_MOVEMENT);
    }
    return movement;
  }

  private static MovementPhase resolveCurrentPhase(final GameData data) {
    if (data.getSequence().size() == 0) {
      return MovementPhase.OTHER;
    }
    if (GameStepPropertiesHelper.isCombatMove(data, true)) {
      return MovementPhase.COMBAT;
    }
    if (GameStepPropertiesHelper.isNonCombatMove(data, true)) {
      return MovementPhase.REDEPLOYMENT;
    }
    return MovementPhase.OTHER;
  }
}
