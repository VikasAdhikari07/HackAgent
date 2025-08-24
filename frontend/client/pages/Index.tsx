import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Header from "@/components/Header";
import { Link } from "react-router-dom";
import { ArrowRight, Lightbulb, Target, Zap } from "lucide-react";

export default function Index() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto text-center max-w-4xl">
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
                AI Strategy Planner
              </h1>
              <p className="text-xl sm:text-2xl text-gray-600 max-w-2xl mx-auto">
                Turn your ideas into actionable plans with AI.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button 
                asChild 
                size="lg" 
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-lg px-8 py-6"
              >
                <Link to="/dashboard" className="flex items-center gap-2">
                  Get Started
                  <ArrowRight className="h-5 w-5" />
                </Link>
              </Button>
              <Button 
                variant="outline" 
                size="lg" 
                asChild
                className="text-lg px-8 py-6 border-purple-200 hover:bg-purple-50"
              >
                <Link to="/about">Learn More</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Transform Ideas into Action
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our AI-powered platform helps you create comprehensive strategies and execute them with precision.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardContent className="p-8 text-center">
                <div className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                  <Lightbulb className="h-8 w-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Smart Prompt Enhancement
                </h3>
                <p className="text-gray-600">
                  Our AI analyzes and enhances your prompts to ensure maximum clarity and effectiveness for strategy generation.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardContent className="p-8 text-center">
                <div className="bg-gradient-to-r from-blue-100 to-indigo-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                  <Target className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Strategic Planning
                </h3>
                <p className="text-gray-600">
                  Generate comprehensive, actionable plans with clear phases, timelines, and measurable outcomes for your goals.
                </p>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardContent className="p-8 text-center">
                <div className="bg-gradient-to-r from-indigo-100 to-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-6">
                  <Zap className="h-8 w-8 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Rapid Execution
                </h3>
                <p className="text-gray-600">
                  Turn your strategies into reality with our execution tools and integrations that streamline implementation.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="container mx-auto text-center max-w-4xl">
          <div className="space-y-8">
            <h2 className="text-3xl sm:text-4xl font-bold text-white">
              Ready to Transform Your Ideas?
            </h2>
            <p className="text-xl text-purple-100">
              Join thousands of professionals who use AI Strategy Planner to turn their vision into actionable results.
            </p>
            <Button 
              asChild 
              size="lg" 
              className="bg-white text-purple-600 hover:bg-gray-50 text-lg px-8 py-6"
            >
              <Link to="/dashboard" className="flex items-center gap-2">
                Start Planning Now
                <ArrowRight className="h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
