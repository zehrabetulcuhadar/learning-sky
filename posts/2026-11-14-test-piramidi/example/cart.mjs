// Pure function: easy to unit test
export function cartTotal(items) {
  let total = 0;
  for (const { price, quantity } of items) {
    if (!Number.isInteger(quantity) || quantity < 1) throw new RangeError("Quantity must be a positive integer");
    if (price < 0) throw new RangeError("Price cannot be negative");
    total += price * quantity;
  }
  const discount = total >= 1000 ? total * 0.1 : 0; // 10% off from 1000 TL
  return Math.round((total - discount) * 100) / 100;
}

// A service with a dependency: tested together with a fake repository
export class CheckoutService {
  constructor(repository) {
    this.repository = repository;
  }
  async checkout(cartId) {
    const items = await this.repository.getItems(cartId);
    if (items.length === 0) throw new Error("Cart is empty");
    const total = cartTotal(items);
    await this.repository.saveOrder({ cartId, total });
    return total;
  }
}
