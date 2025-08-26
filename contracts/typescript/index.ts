





import { z } from 'zod';

// Lot schemas
export const LotSchema = z.object({
  lot_id: z.string().uuid(),
  product_code: z.string(),
  quantity: z.number().int(),
  created_at: z.date()
});

export type Lot = z.infer<typeof LotSchema>;

// ReadyMeal schemas
export const IngredientSchema = z.object({
  name: z.string(),
  lot_id: z.string().uuid(),
  quantity: z.number().int()
});

export const ReadyMealSchema = z.object({
  product_id: z.string().uuid(),
  name: z.string(),
  sku: z.string(),
  ingredients: z.array(IngredientSchema),
  price: z.number()
});

export type Ingredient = z.infer<typeof IngredientSchema>;
export type ReadyMeal = z.infer<typeof ReadyMealSchema>;

// Order schemas
const OrderStatus = z.enum(['PENDING', 'PREPARING', 'READY', 'DELIVERED', 'CANCELLED']);

export const OrderStatusChangedSchema = z.object({
  order_id: z.string().uuid(),
  status: OrderStatus,
  timestamp: z.date()
});

export type OrderStatusChange = z.infer<typeof OrderStatusChangedSchema>;





