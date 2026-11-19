import { test, describe } from "node:test";
import assert from "node:assert/strict";
import { cartTotal, CheckoutService } from "./cart.mjs";

describe("cartTotal (unit)", () => {
  test("sums price times quantity", () => {
    // Arrange
    const items = [{ price: 100, quantity: 2 }, { price: 50, quantity: 1 }];
    // Act
    const total = cartTotal(items);
    // Assert
    assert.equal(total, 250);
  });

  test("gives 10% off at exactly 1000 TL", () => {
    assert.equal(cartTotal([{ price: 500, quantity: 2 }]), 900);
  });

  test("no discount just below 1000 TL", () => {
    assert.equal(cartTotal([{ price: 999.99, quantity: 1 }]), 999.99);
  });

  test("returns 0 for an empty cart", () => {
    assert.equal(cartTotal([]), 0);
  });

  test("rejects a negative quantity", () => {
    assert.throws(() => cartTotal([{ price: 10, quantity: -3 }]), RangeError);
  });
});

describe("CheckoutService (integration with an in-memory repository)", () => {
  class InMemoryRepository {
    carts = { c1: [{ price: 600, quantity: 2 }], empty: [] };
    orders = [];
    async getItems(id) { return this.carts[id] ?? []; }
    async saveOrder(order) { this.orders.push(order); }
  }

  test("calculates the total and saves the order", async () => {
    const repo = new InMemoryRepository();
    const service = new CheckoutService(repo);

    const total = await service.checkout("c1");

    assert.equal(total, 1080);
    assert.deepEqual(repo.orders, [{ cartId: "c1", total: 1080 }]);
  });

  test("refuses an empty cart and saves nothing", async () => {
    const repo = new InMemoryRepository();
    await assert.rejects(new CheckoutService(repo).checkout("empty"), /empty/);
    assert.equal(repo.orders.length, 0);
  });
});
