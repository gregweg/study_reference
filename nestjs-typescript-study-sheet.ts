// ----------------------------------------------
// ✅ TypeScript Class Structure
// ----------------------------------------------
class ExampleClass {
  public name: string;
  private count: number = 0;
  protected status: string = 'active';
  static globalCount = 0;

  constructor(name: string) {
    this.name = name;
    ExampleClass.globalCount++;
  }

  public greet(): string {
    return `Hello, ${this.name}`;
  }

  private log(): void {
    console.log('Internal log');
  }

  protected getStatus(): string {
    return this.status;
  }

  static getCount(): number {
    return ExampleClass.globalCount;
  }
}

// ----------------------------------------------
// Data Structures
// ----------------------------------------------
enum UserRole {
  Admin = 'ADMIN',
  Member = 'MEMBER',
  Guest = 'GUEST',
}

type LoginTuple = [string, Date];

class DataStructuresExample {
  private userArray: string[] = [];
  private userMap: Map<number, string> = new Map();
  private userSet: Set<number> = new Set();
  private loginHistory: LoginTuple[] = [];

  addUser(id: number, name: string) {
    this.userArray.push(name);
    this.userMap.set(id, name);
  }

  logLogin(id: number) {
    const name = this.userMap.get(id);
    if (name) this.loginHistory.push([name, new Date()]);
  }
}

// ----------------------------------------------
// NestJS REST API with TypeORM
// ----------------------------------------------

// Entity (Database Model)
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @Column({ default: 'user' })
  role: string;
}

// Service (Business Logic)
import { Injectable } from '@nestjs/common';

@Injectable()
export class UserService {
  private users: User[] = [];

  createUser(data: Partial<User>): User {
    const user = {
      ...data,
      id: Date.now(),
      role: data.role ?? 'user',
    } as User;

    this.users.push(user);
    return user;
  }

  findAll(): User[] {
    return this.users;
  }

  findOne(id: number): User | undefined {
    return this.users.find(u => u.id === id);
  }

  deleteUser(id: number): boolean {
    const index = this.users.findIndex(u => u.id === id);
    if (index !== -1) {
      this.users.splice(index, 1);
      return true;
    }
    return false;
  }
}

// Controller (REST Endpoints)
import {
  Controller,
  Get,
  Post,
  Delete,
  Param,
  Body,
  HttpException,
  HttpStatus,
} from '@nestjs/common';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  create(@Body() body: Partial<User>): User {
    return this.userService.createUser(body);
  }

  @Get()
  findAll(): User[] {
    return this.userService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): User {
    const user = this.userService.findOne(Number(id));
    if (!user) throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    return user;
  }

  @Delete(':id')
  delete(@Param('id') id: string): string {
    const success = this.userService.deleteUser(Number(id));
    if (!success) throw new HttpException('User not found', HttpStatus.NOT_FOUND);
    return `User ${id} deleted`;
  }
}

// Module (Wires controller + service together)
import { Module } from '@nestjs/common';

@Module({
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}

// App Entry
import { Module as RootModule } from '@nestjs/common';

@RootModule({
  imports: [UserModule],
})
export class AppModule {}