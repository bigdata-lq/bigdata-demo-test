package com.demo.connector.kafka;

import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.clients.consumer.OffsetResetStrategy;

public class CustomerTopicPartitionState {

    private Long position = null;
    private Long highWatermark = null;
    private Long lastStableOffset = null;
    private OffsetAndMetadata committed = null;
    private boolean paused = false;
    private OffsetResetStrategy resetStrategy = null;

    public CustomerTopicPartitionState() {
    }

    private void awaitReset(OffsetResetStrategy strategy) {
        this.resetStrategy = strategy;
        this.position = null;
    }

    public boolean awaitingReset() {
        return this.resetStrategy != null;
    }

    public boolean hasValidPosition() {
        return this.position != null;
    }

    private void seek(long offset) {
        this.position = offset;
        this.resetStrategy = null;
    }

    private void position(long offset) {
        if (!this.hasValidPosition()) {
            throw new IllegalStateException("Cannot set a new position without a valid current position");
        } else {
            this.position = offset;
        }
    }

    private void committed(OffsetAndMetadata offset) {
        this.committed = offset;
    }

    private void pause() {
        this.paused = true;
    }

    private void resume() {
        this.paused = false;
    }

    private boolean isFetchable() {
        return !this.paused && this.hasValidPosition();
    }

    public Long getPosition() {
        return position;
    }

    public Long getHighWatermark() {
        return highWatermark;
    }

    public Long getLastStableOffset() {
        return lastStableOffset;
    }
}
