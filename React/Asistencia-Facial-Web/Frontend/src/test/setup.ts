import "@testing-library/jest-dom";
import { afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => {
    cleanup();
});

class MediaStreamMock {
    getTracks() {
        return [{ stop: vi.fn() }];
    }
}

Object.defineProperty(globalThis.navigator, "mediaDevices", {
    writable: true,
    value: {
        getUserMedia: vi.fn().mockResolvedValue(new MediaStreamMock()),
    },
});


HTMLCanvasElement.prototype.getContext = vi.fn().mockReturnValue({
    drawImage: vi.fn(),
});
HTMLCanvasElement.prototype.toBlob = vi.fn((callback) => {
    callback(new Blob(["fake"], { type: "image/jpeg" }));
});
HTMLCanvasElement.prototype.toDataURL = vi.fn(
    () => "data:image/jpeg;base64,ZmFrZQ=="
);